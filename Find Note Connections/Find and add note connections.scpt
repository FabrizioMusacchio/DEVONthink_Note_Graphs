FasdUAS 1.101.10   ��   ��    k             l     ��  ��      << USER CONFIGURATION >>     � 	 	 2   < <   U S E R   C O N F I G U R A T I O N   > >   
  
 l     ��  ��    0 * Define the name of your Conda environment     �   T   D e f i n e   t h e   n a m e   o f   y o u r   C o n d a   e n v i r o n m e n t      l          j     �� ��  0 conda_env_name CONDA_ENV_NAME  m        �    d t _ p y t h o n  Q K Adjust this to the name of your Conda environment (e.g., "devonthink_env")     �   �   A d j u s t   t h i s   t o   t h e   n a m e   o f   y o u r   C o n d a   e n v i r o n m e n t   ( e . g . ,   " d e v o n t h i n k _ e n v " )      l     ��������  ��  ��        l     ��������  ��  ��        l     ��  ��    5 / --- DO NOT CHANGE ANYTHING BELOW THIS LINE ---     �     ^   - - -   D O   N O T   C H A N G E   A N Y T H I N G   B E L O W   T H I S   L I N E   - - -   ! " ! l     ��������  ��  ��   "  # $ # l   � %���� % O    � & ' & Q   � ( ) * ( k   { + +  , - , l   �� . /��   . ( " Check if any records are selected    / � 0 0 D   C h e c k   i f   a n y   r e c o r d s   a r e   s e l e c t e d -  1 2 1 r     3 4 3 1    ��
�� 
DTsl 4 o      ���� 0 
therecords 
theRecords 2  5 6 5 Z    / 7 8���� 7 =    9 : 9 l    ;���� ; I   �� <��
�� .corecnte****       **** < o    ���� 0 
therecords 
theRecords��  ��  ��   : m    ����   8 k    + = =  > ? > I   (�� @ A
�� .sysodlogaskr        TEXT @ m     B B � C C ` P l e a s e   s e l e c t   a t   l e a s t   o n e   r e c o r d   i n   D E V O N t h i n k . A �� D E
�� 
btns D J      F F  G�� G m     H H � I I  O K��   E �� J K
�� 
dflt J m   ! "����  K �� L��
�� 
disp L m   # $��
�� stic   ��   ?  M�� M L   ) +����  ��  ��  ��   6  N O N l  0 0��������  ��  ��   O  P Q P l  0 0�� R S��   R C = Determine the script directory and construct the Python path    S � T T z   D e t e r m i n e   t h e   s c r i p t   d i r e c t o r y   a n d   c o n s t r u c t   t h e   P y t h o n   p a t h Q  U V U r   0 7 W X W l  0 5 Y���� Y I  0 5�� Z��
�� .earsffdralis        afdr Z  f   0 1��  ��  ��   X o      ����  0 thisscriptfile thisScriptFile V  [ \ [ l  8 I ] ^ _ ] r   8 I ` a ` n   8 E b c b 1   A E��
�� 
psxp c l  8 A d���� d b   8 A e f e l  8 = g���� g c   8 = h i h o   8 9����  0 thisscriptfile thisScriptFile i m   9 <��
�� 
ctxt��  ��   f m   = @ j j � k k  : :��  ��   a o      ���� 0 scriptfolder scriptFolder ^   parent folder    _ � l l    p a r e n t   f o l d e r \  m n m r   J U o p o b   J Q q r q o   J M���� 0 scriptfolder scriptFolder r m   M P s s � t t H s c r i p t s / p y d t _ g e t _ n o t e _ c o n n e c t i o n s . p y p o      ���� (0 python_script_path PYTHON_SCRIPT_PATH n  u v u l  V V��������  ��  ��   v  w x w l  V V�� y z��   y Q K ALTERNATIVELY, define the path absolute to your Python script by yourself:    z � { { �   A L T E R N A T I V E L Y ,   d e f i n e   t h e   p a t h   a b s o l u t e   t o   y o u r   P y t h o n   s c r i p t   b y   y o u r s e l f : x  | } | l  V V�� ~ ��   ~ � � set PYTHON_SCRIPT_PATH to "/Users/YOURUSERNAME/Science/Python/Projekte/DevonThink Note Graphs/Find Note Connections/scripts/pydt_get_note_connections.py"     � � �4   s e t   P Y T H O N _ S C R I P T _ P A T H   t o   " / U s e r s / Y O U R U S E R N A M E / S c i e n c e / P y t h o n / P r o j e k t e / D e v o n T h i n k   N o t e   G r a p h s / F i n d   N o t e   C o n n e c t i o n s / s c r i p t s / p y d t _ g e t _ n o t e _ c o n n e c t i o n s . p y " }  � � � l  V V��������  ��  ��   �  � � � l  V V�� � ���   � < 6 Automatically determine Conda base and source script:    � � � � l   A u t o m a t i c a l l y   d e t e r m i n e   C o n d a   b a s e   a n d   s o u r c e   s c r i p t : �  � � � Q   V � � � � � k   Y r � �  � � � r   Y d � � � I  Y `�� ���
�� .sysoexecTEXT���     TEXT � m   Y \ � � � � � < b a s h   - l   - c   ' c o n d a   i n f o   - - b a s e '��   � o      ���� 0 
conda_base   �  � � � l  e e��������  ��  ��   �  � � � l  e e�� � ���   � V P ALTERNATIVELY, use zsh. By default, we use bash -l -c to emulate a login shell.    � � � � �   A L T E R N A T I V E L Y ,   u s e   z s h .   B y   d e f a u l t ,   w e   u s e   b a s h   - l   - c   t o   e m u l a t e   a   l o g i n   s h e l l . �  � � � l  e e�� � ���   � ] W If your Conda setup is in zsh instead, replace "bash" with "zsh" in the shell command:    � � � � �   I f   y o u r   C o n d a   s e t u p   i s   i n   z s h   i n s t e a d ,   r e p l a c e   " b a s h "   w i t h   " z s h "   i n   t h e   s h e l l   c o m m a n d : �  � � � l  e e�� � ���   � G Aset conda_base to do shell script "zsh -l -c 'conda info --base'"    � � � � � s e t   c o n d a _ b a s e   t o   d o   s h e l l   s c r i p t   " z s h   - l   - c   ' c o n d a   i n f o   - - b a s e ' " �  � � � l  e e�� � ���   � 5 /display dialog "Conda base path: " & conda_base    � � � � ^ d i s p l a y   d i a l o g   " C o n d a   b a s e   p a t h :   "   &   c o n d a _ b a s e �  � � � l  e e��������  ��  ��   �  � � � r   e p � � � b   e l � � � o   e h���� 0 
conda_base   � m   h k � � � � � . / e t c / p r o f i l e . d / c o n d a . s h � o      ���� 0 conda_sh_path CONDA_SH_PATH �  � � � l  q q��������  ��  ��   �  � � � l  q q�� � ���   � � � ALTERNATIVELY, define the path to your Conda installation by yourself; you can find it by running "conda info --base" in the terminal, e.g., "/Users/YOUR_USERNAME/miniforge3". Then append "/etc/profile.d/conda.sh" and enter the full path here.    � � � ��   A L T E R N A T I V E L Y ,   d e f i n e   t h e   p a t h   t o   y o u r   C o n d a   i n s t a l l a t i o n   b y   y o u r s e l f ;   y o u   c a n   f i n d   i t   b y   r u n n i n g   " c o n d a   i n f o   - - b a s e "   i n   t h e   t e r m i n a l ,   e . g . ,   " / U s e r s / Y O U R _ U S E R N A M E / m i n i f o r g e 3 " .   T h e n   a p p e n d   " / e t c / p r o f i l e . d / c o n d a . s h "   a n d   e n t e r   t h e   f u l l   p a t h   h e r e . �  ��� � l  q q�� � ���   � T N set CONDA_SH_PATH to "/Users/YOURUSERNAME/miniforge3/etc/profile.d/conda.sh"     � � � � �   s e t   C O N D A _ S H _ P A T H   t o   " / U s e r s / Y O U R U S E R N A M E / m i n i f o r g e 3 / e t c / p r o f i l e . d / c o n d a . s h "  ��   � R      ������
�� .ascrerr ****      � ****��  ��   � k   z � � �  � � � I  z ��� � �
�� .sysodlogaskr        TEXT � m   z } � � � � � � C o u l d   n o t   d e t e r m i n e   t h e   C o n d a   b a s e   p a t h .   P l e a s e   m a k e   s u r e   ' c o n d a '   i s   a v a i l a b l e   i n   y o u r   s h e l l   e n v i r o n m e n t . � �� � �
�� 
btns � J   ~ � � �  ��� � m   ~ � � � � � �  O K��   � �� � �
�� 
dflt � m   � �����  � �� ���
�� 
disp � m   � ���
�� stic    ��   �  ��� � L   � �����  ��   �  � � � l  � ���������  ��  ��   �  � � � l  � ��� � ���   � "  Construct the shell command    � � � � 8   C o n s t r u c t   t h e   s h e l l   c o m m a n d �  � � � r   � � � � � m   � � � � � � �   � o      ���� 0 shell_command   �  � � � l  � ��� � ���   � a [ IMPORTANT: Use 'bash -c' for execution so that 'source' and 'conda activate' work properly    � � � � �   I M P O R T A N T :   U s e   ' b a s h   - c '   f o r   e x e c u t i o n   s o   t h a t   ' s o u r c e '   a n d   ' c o n d a   a c t i v a t e '   w o r k   p r o p e r l y �  � � � r   � � � � � b   � � � � � b   � � � � � o   � ����� 0 shell_command   � m   � � � � � � �  b a s h   - c   � n   � � � � � 1   � ���
�� 
strq � l 	 � � ����� � l  � � ����� � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � b   � � � � � m   � � � � �    s o u r c e   � n   � � 1   � ���
�� 
strq o   � ����� 0 conda_sh_path CONDA_SH_PATH � m   � � �    & &   � l 	 � ����� m   � � �  c o n d a   a c t i v a t e  ��  ��   � n   � �	 1   � ���
�� 
strq	 o   � �����  0 conda_env_name CONDA_ENV_NAME � m   � �

 �    & &   � l 	 � ����� m   � � �  p y t h o n  ��  ��   � n   � � 1   � ���
�� 
strq l 
 � ����� o   � ����� (0 python_script_path PYTHON_SCRIPT_PATH��  ��  ��  ��  ��  ��   � o      ���� 0 shell_command   �  l  � ���������  ��  ��    l  � �����      Execute the shell command    � 4   E x e c u t e   t h e   s h e l l   c o m m a n d  I  � ���~
� .sysoexecTEXT���     TEXT o   � ��}�} 0 shell_command  �~    l  � ��|�{�z�|  �{  �z    l  � ��y !�y    Y S Optionally, write the constructed shell command to a temporary file for debugging:   ! �"" �   O p t i o n a l l y ,   w r i t e   t h e   c o n s t r u c t e d   s h e l l   c o m m a n d   t o   a   t e m p o r a r y   f i l e   f o r   d e b u g g i n g : #$# l  � ��x%&�x  % q k do shell script "echo " & quoted form of shell_command & " > ~/Desktop/devonthink_shell_command_debug.txt"   & �'' �   d o   s h e l l   s c r i p t   " e c h o   "   &   q u o t e d   f o r m   o f   s h e l l _ c o m m a n d   &   "   >   ~ / D e s k t o p / d e v o n t h i n k _ s h e l l _ c o m m a n d _ d e b u g . t x t "$ ()( l  � ��w�v�u�w  �v  �u  ) *+* l  � ��t�s�r�t  �s  �r  + ,-, l  � ��q./�q  . . ( Notification after successful execution   / �00 P   N o t i f i c a t i o n   a f t e r   s u c c e s s f u l   e x e c u t i o n- 121 r   � �343 m   � �55 �66  4 o      �p�p 0 	filenames 	fileNames2 787 X   �9�o:9 r   �;<; b   �=>= b   �?@? o   � ��n�n 0 	filenames 	fileNames@ n   �ABA 1   ��m
�m 
pnamB o   � ��l�l 0 r  > m  CC �DD  ,  < o      �k�k 0 	filenames 	fileNames�o 0 r  : o   � ��j�j 0 
therecords 
theRecords8 EFE l �i�h�g�i  �h  �g  F GHG l �fIJ�f  I "  Remove last comma and space   J �KK 8   R e m o v e   l a s t   c o m m a   a n d   s p a c eH LML Z  7NO�e�dN ?  PQP n  RSR 1  �c
�c 
lengS o  �b�b 0 	filenames 	fileNamesQ m  �a�a O r  3TUT n  /VWV 7 !/�`XY
�` 
ctxtX m  ')�_�_ Y m  *.�^�^��W o  !�]�] 0 	filenames 	fileNamesU o      �\�\ 0 	filenames 	fileNames�e  �d  M Z[Z l 88�[�Z�Y�[  �Z  �Y  [ \]\ l 88�X^_�X  ^ J D Truncate if too long for notification (rough limit ~120 characters)   _ �`` �   T r u n c a t e   i f   t o o   l o n g   f o r   n o t i f i c a t i o n   ( r o u g h   l i m i t   ~ 1 2 0   c h a r a c t e r s )] aba Z  8ccd�W�Vc l 8Ce�U�Te ?  8Cfgf n  8?hih 1  ;?�S
�S 
lengi o  8;�R�R 0 	filenames 	fileNamesg m  ?B�Q�Q x�U  �T  d r  F_jkj b  F[lml n  FWnon 7 IW�Ppq
�P 
ctxtp m  OQ�O�O q m  RV�N�N uo o  FI�M�M 0 	filenames 	fileNamesm m  WZrr �ss  &k o      �L�L 0 	filenames 	fileNames�W  �V  b tut l dd�K�J�I�K  �J  �I  u vwv I dy�Hxy
�H .sysonotfnull��� ��� TEXTx o  dg�G�G 0 	filenames 	fileNamesy �Fz{
�F 
apprz m  jm|| �}}  D E V O N t h i n k{ �E~�D
�E 
subt~ m  ps ��� 0 N o t e   c o n n e c t i o n s   u p d a t e d�D  w ��� l zz�C�B�A�C  �B  �A  � ��@� l zz�?�>�=�?  �>  �=  �@   ) R      �<��
�< .ascrerr ****      � ****� o      �;�; 0 errmsg errMsg� �:��9
�: 
errn� o      �8�8 0 errnum errNum�9   * I ���7��
�7 .sysodlogaskr        TEXT� b  ����� b  ����� b  ����� b  ����� m  ���� ��� F E r r o r   e x e c u t i n g   t h e   P y t h o n   s c r i p t :  � o  ���6�6 0 errmsg errMsg� m  ���� ���    ( E r r o r   c o d e :  � o  ���5�5 0 errnum errNum� m  ���� ���  )� �4��
�4 
btns� J  ���� ��3� m  ���� ���  O K�3  � �2��
�2 
dflt� m  ���1�1 � �0��/
�0 
disp� m  ���.
�. stic    �/   ' 5     �-��,
�- 
capp� m    �� ��� : c o m . d e v o n - t e c h n o l o g i e s . t h i n k 3
�, kfrmID  ��  ��   $ ��+� l     �*�)�(�*  �)  �(  �+       �'� ��'  � �&�%�&  0 conda_env_name CONDA_ENV_NAME
�% .aevtoappnull  �   � ****� �$��#�"���!
�$ .aevtoappnull  �   � ****� k    ���  #� �   �#  �"  � ���� 0 r  � 0 errmsg errMsg� 0 errnum errNum� @������ B� H�������� j�� s� ���
 ��	�� � �� �� � ��
5���� C��������r��|�������������
� 
capp
� kfrmID  
� 
DTsl� 0 
therecords 
theRecords
� .corecnte****       ****
� 
btns
� 
dflt
� 
disp
� stic   � 
� .sysodlogaskr        TEXT
� .earsffdralis        afdr�  0 thisscriptfile thisScriptFile
� 
ctxt
� 
psxp� 0 scriptfolder scriptFolder� (0 python_script_path PYTHON_SCRIPT_PATH
� .sysoexecTEXT���     TEXT�
 0 
conda_base  �	 0 conda_sh_path CONDA_SH_PATH�  �  
� stic    � 0 shell_command  
� 
strq� 0 	filenames 	fileNames
� 
kocl
� 
cobj
�  
pnam
�� 
leng������ x�� u
�� 
appr
�� 
subt�� 
�� .sysonotfnull��� ��� TEXT�� 0 errmsg errMsg� ������
�� 
errn�� 0 errnum errNum��  �!�)���0�u*�,E�O�j j  ���kv�k��� OhY hO)j E�O�a &a %a ,E` O_ a %E` O a j E` O_ a %E` OPW X  a �a kv�k�a � OhOa  E` !O_ !a "%a #_ a $,%a %%a &%b   a $,%a '%a (%_ a $,%a $,%E` !O_ !j Oa )E` *O )�[a +a ,l kh  _ *�a -,%a .%E` *[OY��O_ *a /,l _ *[a \[Zk\Za 02E` *Y hO_ *a /,a 1 _ *[a \[Zk\Za 22a 3%E` *Y hO_ *a 4a 5a 6a 7a 8 9OPW &X : ;a <�%a =%�%a >%�a ?kv�k�a � U ascr  ��ޭ