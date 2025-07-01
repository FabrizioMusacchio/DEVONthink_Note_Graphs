"""
This is the main script to generate a note connection graph in DEVONthink 3 
using Python and PyVis.

Install the required Python packages in a Conda environment named `dt_python`:

conda create -n dt_python python=3.10 mamba -y
conda activate dt_python
mamba install ipykernel numpy joblib tqdm -y
pip install pydt3 pyvis networkx
"""
# %% IMPORTS
from pydt3 import DEVONthink3
import os
from pyvis.network import Network
from tqdm import tqdm
import numpy as np
import networkx as nx
import re

# imports for parallelization:
from joblib import Parallel, delayed
import multiprocessing

# deactivate warnings:
import warnings
warnings.filterwarnings("ignore")
# %% DEFINE PARAMETERS

# adjust max_graph_nodes if needed for scaling threshold:
MAX_NODES_FOR_DEFAULT_PHYSICS = 100 # threshold for larger graphs to adjust physics settings

# %% FUNCTIONS

# define the parallel function to get cross-links for a given record UUID
def get_cross_links_for_record_parallel(record_uuid, valid_target_uuids_local):
    """
    Fetches outgoing wiki links for a given record UUID
    and filters them based on the valid_target_uuids.
    """
    worker_dt3 = DEVONthink3() # Each worker must create its own instance

    try:
        record_obj = worker_dt3.get_record_with_uuid(record_uuid)
    except Exception as e:
        # print(f"Warning (Worker): Could not retrieve record object for UUID {record_uuid}. Skipping. Error: {e}")
        return [] # Return empty list if the record can't be retrieved
    
    current_record_edges = []
    
    outgoing_links = record_obj.outgoing_wiki_references()
    outgoing_links = [link for link in outgoing_links if link.type == "markdown"]
    outgoing_links = list({file.uuid: file for file in outgoing_links}.values()) # Deduplicate by UUID
    
    for link in outgoing_links:
        if link.uuid in valid_target_uuids_local and link.uuid != record_obj.uuid:
            current_record_edges.append((record_obj.uuid, link.uuid))
            
    return current_record_edges


# %% MAIN
# start multiprocessing with 'spawn' method:
multiprocessing.set_start_method('spawn', force=True)

# get the current active DEVONthink3 instance(s)
dt3 = DEVONthink3()

# verify that we have at least one selected record in DEVONthink:
if len (dt3.selected_records) == 0:
    _  = dt3.display_dialog("Find note connections:\nNo records selected in DEVONthink. Please select a record first.",
                    buttons=["OK"],
                    default_button="OK", 
                    with_icon="caution")
    raise ValueError("No records selected in DEVONthink. Please select a record first.")

# check whether there is a TagFolder/folder exactly called "_nlinks"; if not, create it in the global inbox:
dt_folder_name = "_nlinks"
folder_search_results = dt3.search(dt_folder_name)
# there should be only ONE folder with this name:
if len(folder_search_results) >= 1:
    folder_search_results = [record for record in folder_search_results if record.name == dt_folder_name]
    dt_folder_UUID = folder_search_results[0].uuid
else:
    # create the folder in the currently selected database:
    dt_folder = dt3.create_location(dt_folder_name, dt3.selected_records[0].database)
    dt_folder_UUID = dt_folder.uuid

# get currently selected records and their properties:
selected_records = dt3.selected_records
selected_records_uuid = [rec.uuid for rec in selected_records]
selected_records_names = [rec.name for rec in selected_records]
selected_records_types = [rec.type for rec in selected_records]
selected_records_outgoing_wiki_references = [rec.outgoing_wiki_references() for rec in selected_records]
selected_records_incoming_wiki_references = [rec.incoming_wiki_references() for rec in selected_records]

# %% START LOOP OVER SELECTED RECORDS
for selected_record_i in range(len(selected_records)):
    # selected_record_i = 0
    print(f"Processing selected record {selected_record_i+1}/{len(selected_records)}...")
    
    # %% LOAD CURRENT RECORD PROPERTIES:
    selected_record_name = selected_records_names[selected_record_i]
    selected_record_uuid = selected_records_uuid[selected_record_i]
    selected_record_type = selected_records_types[selected_record_i]
    selected_record_outgoing_wiki_references = selected_records_outgoing_wiki_references[selected_record_i]
    selected_record_incoming_wiki_references = selected_records_incoming_wiki_references[selected_record_i]

    print(f"Selected Record {selected_record_i+1}: {selected_record_name}")
    print(f"Type: {selected_record_type}")
    print(f"UUID: {selected_record_uuid}")
    # print(f"Outgoing Wiki References: {[ref.name for ref in selected_record_outgoing_wiki_references]}")
    # print(f"Incoming Wiki References: {[ref.name for ref in selected_record_incoming_wiki_references]}")
    print("-" * 40)
    
    # verify that the selected record is a markdown file, otherwise skip it:
    if selected_record_type != "markdown":
        print(f"Skipping record {selected_record_name} (UUID: {selected_record_uuid}) because it is not a markdown file.")
        continue

    # fetch selected_record's outgoing and incoming wiki references:
    outgoing_wiki_references = selected_record_outgoing_wiki_references
    outgoing_wiki_references = [ref for ref in outgoing_wiki_references if ref.type == "markdown"]
    outgoing_wiki_references = list({file.uuid: file for file in outgoing_wiki_references}.values()) # Deduplicate by UUID, not name
    #print(f"Outgoing markdown files: {[file.name for file in outgoing_wiki_references]}")

    incoming_wiki_references = selected_record_incoming_wiki_references
    incoming_wiki_references = [ref for ref in incoming_wiki_references if ref.type == "markdown"]
    incoming_wiki_references = [file for file in incoming_wiki_references if not file.name.startswith("nlink_")]
    #print(f"Incoming markdown files without nlink: {[file.name for file in incoming_wiki_references]}")

    # create a list of all outgoing and incoming wiki links:
    selected_record_wikilinks_all = list({file.uuid: file for file in outgoing_wiki_references + incoming_wiki_references}.values()) # Deduplicate by UUID
    #print(f"selected_record_wikilinks_all: {[file.name for file in selected_record_wikilinks_all]}")

    # collect all UUIDs that will be nodes in our graph, including the main node
    all_node_uuids = set([selected_record_uuid] + [rec.uuid for rec in selected_record_wikilinks_all])
    # Create a mapping from UUID to record object for efficient lookup (needed later for labels/titles)
    # This mapping will be used in the main thread for Pyvis node creation,
    # but NOT directly passed to the parallel function.
    uuid_to_record_obj = {rec.uuid: rec for rec in selected_record_wikilinks_all}
    uuid_to_record_obj[selected_record_uuid] = dt3.get_record_with_uuid(selected_record_uuid)

    # calculate the number of nodes:
    num_nodes = len(all_node_uuids)

    # %% PRE-CALCULATE EDGES AND NODE SIZES (Parallel with joblib)
    edges = []
    # add initial edges from/to the selected_record:
    for link in outgoing_wiki_references:
        edges.append((selected_record_uuid, link.uuid))
    for link in incoming_wiki_references:
        edges.append((link.uuid, selected_record_uuid))

    # use a set for faster checking of existing edges:
    existing_edges_set = set(edges) 

    # prepare valid target UUIDs for efficient lookup (will be passed to parallel function):
    valid_target_uuids = set([rec.uuid for rec in selected_record_wikilinks_all])
    valid_target_uuids.add(selected_record_uuid)

    print("Starting parallel processing for cross-links with joblib...")

    # Determine the number of parallel jobs (number of CPU cores)
    n_jobs = os.cpu_count()
    if n_jobs is None: # Fallback for systems where os.cpu_count() might return None
        n_jobs = 4 # Default to 4 if cannot determine

    # parallel processing with joblib...
    # `backend='loky'` is the default setting for processes and is usually the best choice.
    # `tqdm` is used directly via the `Parallel` object to provide a progress bar.
    results_lists_of_edges = Parallel(n_jobs=n_jobs)(
        delayed(get_cross_links_for_record_parallel)(record_uuid, valid_target_uuids)
        for record_uuid in tqdm(list(all_node_uuids), desc="Getting cross-links")
    )

    print("Finished parallel processing for cross-links.")

    # Merge results and add to edges
    for edge_list in results_lists_of_edges:
        for new_edge in edge_list:
            if new_edge not in existing_edges_set: # Avoid duplicates
                edges.append(new_edge)
                existing_edges_set.add(new_edge)
    edges = sorted(list(set(edges)))

    # determine node sizes based on degree (number of connections):
    node_sizes = {}
    # Initialize all known nodes with a base size (e.g., 1)
    for record_uuid in all_node_uuids:
        node_sizes[record_uuid] = 1 # Base size

    # count how many times each node appears in edges (degree):
    for src, tgt in edges:
        node_sizes[src] = node_sizes.get(src, 0) + 1
        node_sizes[tgt] = node_sizes.get(tgt, 0) + 1

    median_top_25_percent = np.median(sorted(node_sizes.values(), reverse=True)[:max(1, len(node_sizes) // 4)]) # At least 1 to avoid division by zero

    # scale node sizes to a range of 10 to 30:
    if len(all_node_uuids)> MAX_NODES_FOR_DEFAULT_PHYSICS:
        # For larger graphs, use a wider range
        min_target_size = 2.5 # Minimum size for larger graphs
        max_target_size = 40 # Maximum size for larger graphs
    else:
        min_target_size = 2.5
        max_target_size = 20

    node_sizes_for_scaling = {k: v for k, v in node_sizes.items() if k != selected_record_uuid}

    if node_sizes_for_scaling: # Only calculate min/max if there are other nodes
        min_current_size = min(node_sizes_for_scaling.values())
        max_current_size = max(node_sizes_for_scaling.values())
    else: # Fallback if only the selected node exists
        min_current_size = 1
        max_current_size = 1

    current_size_range = max_current_size - min_current_size
    target_size_range = max_target_size - min_target_size

    for key in node_sizes:
        if current_size_range == 0: # Handle case with all (other) nodes having same size
            node_sizes[key] = int(min_target_size + target_size_range / 2) # Set to middle of target range
        else:
            #node_sizes[key] = int((node_sizes[key] - min_current_size) / current_size_range * target_size_range + min_target_size)
            
            scaled_size = (node_sizes[key] - min_current_size) / current_size_range * target_size_range + min_target_size
            node_sizes[key] = int(max(min_target_size, min(max_target_size, scaled_size)))

    # %% CALCULATE INITIAL NODE POSITIONS WITH NETWORKX

    # create a NetworkX graph for layout calculation:
    G_layout = nx.Graph() # Undirected for force-directed layout

    # add all nodes to the NetworkX graph:
    for uuid in all_node_uuids:
        # Ensure node exists in node_sizes, provide a default if not (e.g., 1)
        G_layout.add_node(uuid, mass=node_sizes.get(uuid, 1))

    # add edges to the NetworkX graph (undirected for spring_layout):
    for src, tgt in edges:
        G_layout.add_edge(src, tgt)

    # determine the internal canvas size for NetworkX based on the number of nodes:
    BASE_CANVAS_WIDTH = 1000 # Increased base for better spread
    BASE_CANVAS_HEIGHT = 800 # Increased base for better spread

    BASE_CANVAS_WIDTH_LARGE = 6000 # For larger graphs
    BASE_CANVAS_HEIGHT_LARGE = 3000 # For larger graphs

    if num_nodes > MAX_NODES_FOR_DEFAULT_PHYSICS: # Use this threshold for scaling internal canvas
        fixed_canvas_width = min(BASE_CANVAS_WIDTH + (num_nodes - MAX_NODES_FOR_DEFAULT_PHYSICS) * 50, BASE_CANVAS_WIDTH_LARGE)
        fixed_canvas_height = min(BASE_CANVAS_HEIGHT + (num_nodes - MAX_NODES_FOR_DEFAULT_PHYSICS) * 40, BASE_CANVAS_HEIGHT_LARGE)
        k_value = 0.05 # Slightly larger k for larger graphs
        # larger value of k spreads nodes more, smaller values cluster them closer
        max_iter_fa2 = 4000
    else:
        fixed_canvas_width = BASE_CANVAS_WIDTH
        fixed_canvas_height = BASE_CANVAS_HEIGHT
        k_value = 0.15 # Default k for smaller graphs
        max_iter_fa2 = 10

    # calculate positions using spring_layout:
    print("Calculating node positions with NetworkX...")
    pos_nx = nx.spring_layout(G_layout,
                            iterations=500, # Increased iterations for better stability
                            k=k_value,
                            weight='mass', # Use node sizes as weight
                            seed=42) # For reproducibility
    """ pos_nx = nx.forceatlas2_layout(G_layout,
                            max_iter=max_iter_fa2,
                            jitter_tolerance=10.0,
                            gravity=0.02,  #0.1
                            seed=42,
                            scaling_ratio=100.0,
                            linlog=True
                        ) """
    """ 
    scaling_ratio:  Affects the distance between nodes. increased values spread 
                    nodes further apart.
    gravity: Affects how strongly nodes are attracted to each other. 
                    smaller values cluster nodes closer together.
    jitter_tolerance: Controls how much nodes can move around.
    linlog: If True, uses a lin-log force model which can help with larger graphs.
    """


    # scale NetworkX positions to Pyvis coordinate system:
    min_nx_x = min(p[0] for p in pos_nx.values())
    max_nx_x = max(p[0] for p in pos_nx.values())
    min_nx_y = min(p[1] for p in pos_nx.values())
    max_nx_y = max(p[1] for p in pos_nx.values())

    nx_range_x = max_nx_x - min_nx_x
    nx_range_y = max_nx_y - min_nx_y

    target_padding_factor = 0.1 # 10% padding
    target_width = fixed_canvas_width * (1 - 2 * target_padding_factor)
    target_height = fixed_canvas_height * (1 - 2 * target_padding_factor)

    if nx_range_x == 0: nx_range_x = 1
    if nx_range_y == 0: nx_range_y = 1

    scale_factor_x = target_width / nx_range_x
    scale_factor_y = target_height / nx_range_y
    scale_factor = min(scale_factor_x, scale_factor_y)

    translate_x = fixed_canvas_width * target_padding_factor - min_nx_x * scale_factor
    translate_y = fixed_canvas_height * target_padding_factor - min_nx_y * scale_factor

    node_positions_pyvis = {}
    for uuid, (nx_x, nx_y) in pos_nx.items():
        pyvis_x = nx_x * scale_factor + translate_x
        pyvis_y = nx_y * scale_factor + translate_y
        #node_positions_pyvis[uuid] = {'x': pyvis_x, 'y': pyvis_y}
        node_positions_pyvis[uuid] = {'x': float(pyvis_x), 'y': float(pyvis_y)} 

    print("Node positions calculated.")

    # %% GENERATE GRAPH WITH PYVIS (using pre-calculated positions)
    # create a Pyvis Network object with the calculated positions:
    pyvis_height = "400px" 
    if num_nodes > MAX_NODES_FOR_DEFAULT_PHYSICS:
        # set the maximum height for the Pyvis container to a smaller value, e.g., 500px
        pyvis_height = f"{min(fixed_canvas_height + 100, 500)}px"
    else:
        pyvis_height = "400px" # for smaller graphs


    net = Network(
        notebook=True,
        height=pyvis_height,
        width="100%",
        directed=True,
        cdn_resources="in_line",
        bgcolor="white",
        font_color="black",
    )

    if num_nodes > MAX_NODES_FOR_DEFAULT_PHYSICS:
        net.force_atlas_2based(
            gravity=-6, # Adjusted for larger graphs
            central_gravity=0.02, # Reduced for larger graphs
            spring_length=100, # Reduced for larger graphs
            spring_strength=0.08, # Reduced for larger graphs
            damping=0.4, # Adjusted for larger graphs
        )
        net.toggle_physics(False)
        net.show_buttons(filter_=['physics'])
        ARROW_OPACITY = 0.2 # Set a default opacity for arrows
    else:
        net.repulsion(node_distance=100, central_gravity=0.2, 
                    spring_length=200, spring_strength=0.05)
        net.toggle_physics(False)
        net.show_buttons(filter_=['physics'])
        ARROW_OPACITY = 0.8 # Set a default opacity for arrows

    # Add nodes with pre-calculated positions
    # Use the mapping from original UUIDs to node objects for labels/titles

    # main node:
    main_node_data = node_positions_pyvis.get(selected_record_uuid, {'x': 0, 'y': 0})
    # set main_node_size to the average of 25% largest node sizes
    node_sizes_sorted = sorted(node_sizes.values(), reverse=True)
    main_node_size = int(np.mean(node_sizes_sorted[:max(1, len(node_sizes_sorted) // 10)])) # At least 1 to avoid division by zero
    if main_node_size < 10: # Ensure a minimum size for visibility
        main_node_size = 10 # Minimum size for the main node
    net.add_node(
        selected_record_uuid, 
        label=selected_record_name, 
        title=f'<a href="x-devonthink-item://{selected_record_uuid}" target="_blank">{selected_record_name}</a>', 
        color="#FFF837", 
        url=f"x-devonthink-item://{selected_record_uuid}", 
        size=main_node_size,
        x=main_node_data['x'],
        y=main_node_data['y'],
        fixed=False # Optionally fix the main node to keep it central for initial view
    )

    # all other nodes:
    for uuid in all_node_uuids:
        if uuid == selected_record_uuid:
            continue 

        record = uuid_to_record_obj.get(uuid)
        if record:
            node_pos_data = node_positions_pyvis.get(uuid, {'x': 0, 'y': 0})
            # shorten the record name if it is longer than 20 characters and add "..." at the end
            record_name_use = record.name
            if len(record_name_use) > 20:
                record_name_use = record_name_use[:17] + "..."
            net.add_node(
                record.uuid, 
                label=record_name_use, 
                title=f'<a href="x-devonthink-item://{record.uuid}" target="_blank">{record.name}</a>', 
                color="#ADD8E6", 
                url=f"x-devonthink-item://{record.uuid}", 
                size=node_sizes[record.uuid],
                x=node_pos_data['x'],
                y=node_pos_data['y'],
                fixed=False # Nodes are fixed if physics is disabled globally
            )
        else:
            print(f"Warning: Record object not found for UUID {uuid}. Skipping node creation.")

                
    # Add edges
    # Re-initialize added_edges set to prevent duplicates, as 'edges' might have grown.
    added_edges = set() 

    for source_uuid, target_uuid in edges:
        if (source_uuid, target_uuid) in added_edges:
            continue
        
        # Determine edge color based on relationship to main_node_uuid
        #edge_color = "lightgray" # Default color
        edge_color = f"rgba(211,211,211,{ARROW_OPACITY})" # Default color, lightgray with 30% opacity

        
        is_main_node_source = (source_uuid == selected_record_uuid)
        is_main_node_target = (target_uuid == selected_record_uuid)
        
        if is_main_node_source and not is_main_node_target:
            # Link from main node to another node
            # Check if inverse link exists (target -> source)
            if (target_uuid, source_uuid) in existing_edges_set: # Use the set for quick check
                #edge_color = "blue" # Mutual link
                edge_color = f"rgba(0,0,255,{ARROW_OPACITY})"
            else:
                #edge_color = "green" # One-way from main node
                edge_color = f"rgba(0,255,0,{ARROW_OPACITY})" # One-way from main node, green with 30% opacity
        elif not is_main_node_source and is_main_node_target:
            # Link from another node to main node
            # Check if inverse link exists (main node -> source)
            if (target_uuid, source_uuid) in existing_edges_set: # Use the set for quick check
                #edge_color = "blue" # Mutual link
                edge_color = f"rgba(0,0,255,{ARROW_OPACITY})"
            else:
                #edge_color = "orange" # One-way to main node
                edge_color = f"rgba(255,165,0,{ARROW_OPACITY})" # One-way to main node, orange with 30% opacity

        net.add_edge(source_uuid, target_uuid, color=edge_color)
        added_edges.add((source_uuid, target_uuid))


    html_code = net.generate_html()

    # in html_code, search for "div.vis-configuration.vis-config-option-container{background-color:#fff";
    # if present, replace it with "div.vis-configuration.vis-config-option-container{background-color:CanvasText":
    html_code = re.sub(r'div\.vis-configuration\.vis-config-option-container\s*{background-color:#fff', 
                        'div.vis-configuration.vis-config-option-container{background-color:CanvasText', 
                        html_code, flags=re.IGNORECASE)
    #"div.vis-configuration.vis-config-option-container{background-color:#fff" in html_code

    # --- Patch: JavaScript-Injection for click handler ---
    js_injection = """
    <script type="text/javascript">
    window.addEventListener('DOMContentLoaded', function() {
        if (typeof network !== 'undefined') {
            network.on("click", function(params) {
                if (params.nodes.length > 0) {
                    var nodeId = params.nodes[0];
                    var nodeData = network.body.data.nodes.get(nodeId);

                    if (nodeData && nodeData.url) {
                        window.open(nodeData.url, '_blank');
                        console.log("URL opened:", nodeData.url);
                    } else {
                        console.log("Clicked node has no URL or data not found.");
                    }
                }
            });

            network.on("hoverNode", function(params) {
                var nodeId = params.node;
                var nodeData = network.body.data.nodes.get(nodeId);
                if (nodeData && nodeData.url) {
                    network.canvas.body.container.style.cursor = 'pointer';
                }
            });

            network.on("blurNode", function(params) {
                network.canvas.body.container.style.cursor = 'default';
            });

        }
    });
    </script>
    """

    html_code = html_code.replace("</body>", js_injection + "\n</body>")

    # %% WRITE HTML FILE INTO DEVONthink
    # write the html file into DT:
    new_html_filename = "nlink_" + selected_record_uuid
    existing_records = dt3.search(new_html_filename, dt3.get_record_with_uuid(dt_folder_UUID))
    if len(existing_records) >= 1:
        existing_records = [record for record in existing_records if record.name == new_html_filename]

    if existing_records:
        print(f"File with name {new_html_filename} already exists in DT. We will delete them first.")
        for record in existing_records:
            dt3.delete(record)

    print(f"File with name {new_html_filename} does not exist in DT. We will create it.")

    record = dt3.create_record_with({
        'name': new_html_filename,
        'type': 'html',
        'plain text': html_code,
    }, dt3.get_record_with_uuid(dt_folder_UUID))
    new_html_filename_uuid = record.uuid
    
    """ SCAN N­OTE'S CONTENT AND REPLACE/APPEND IFRAME:
    now, scan the actual note's content for the following pattern/entry:
    <iframe src="x-devonthink-item://SOME_UUID" width="100%" height="580px" frameborder="0" allowfullscreen></iframe>

    If present, replace it with the new HTML file's UUID: if not present, append it to the end of the note's content.
    """
    if num_nodes > MAX_NODES_FOR_DEFAULT_PHYSICS:
        iframe_pattern = re.compile(
            r'<iframe\s+src="x-devonthink-item://[A-Z0-9\-]+"\s+width="100%" height="580px" frameborder="0" allowfullscreen></iframe>',
            re.IGNORECASE)
        new_iframe = f'<iframe src="x-devonthink-item://{new_html_filename_uuid}" width="100%" height="580px" frameborder="0" allowfullscreen></iframe>'
    else:
        iframe_pattern = re.compile(
            r'<iframe\s+src="x-devonthink-item://[A-Z0-9\-]+"\s+width="100%" height="480px" frameborder="0" allowfullscreen></iframe>',
            re.IGNORECASE)
        new_iframe = f'<iframe src="x-devonthink-item://{new_html_filename_uuid}" width="100%" height="480px" frameborder="0" allowfullscreen></iframe>'

    selected_record_plain_text = dt3.get_record_with_uuid(selected_record_uuid).plain_text

    if iframe_pattern.search(selected_record_plain_text):
        # Replace existing iframe with new one
        new_content = iframe_pattern.sub(new_iframe, selected_record_plain_text)
        print("Existing iframe found and replaced with new HTML file's UUID.")
    else:
        # Append new iframe at the end
        new_content = selected_record_plain_text + "\n\n## Note connections\n" + new_iframe + "\n\n"
        print("No existing iframe found. Appended new iframe to the end of the note.")

    """ INSERT NLINK LINK AT THE BOTTOM OF THE N­OTE:
    Right before the iframe pattern, check if the following markdown code is present:
    
    [Open note connections file (nlink)](x-devonthink-item://[SOME_UUID])
    
    if present, replace it with the new HTML file's UUID. If not present, insert it right after the <body> tag.
    """
    nlink_pattern = re.compile(
        r'\[Open note connections file \(nlink\)\]\(x-devonthink-item://[A-Z0-9\-]+\)',
        re.IGNORECASE)

    if nlink_pattern.search(new_content):
        # Replace existing nlink with new one
        new_nlink = f'[Open note connections file (nlink)](x-devonthink-item://{new_html_filename_uuid})'
        new_content = nlink_pattern.sub(new_nlink, new_content)
        print("Existing nlink found and replaced with new HTML file's UUID.")
    else:
        # Insert new nlink below the just inserted or updated iframe pattern:
        new_nlink = f'[Open note connections file (nlink)](x-devonthink-item://{new_html_filename_uuid})'
        new_content = new_content +  new_nlink
        print("No existing nlink found. Inserted new nlink to the note.")
        
    # Update the record with the new content
    dt3.get_record_with_uuid(selected_record_uuid).plain_text = new_content

print("All selected records processed successfully. Note connections updated.")
# %% END