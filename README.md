# fsf_2019_screening_task2

Steps to run this application :<br/>
1] Download and extract all the files in a folder<br/>
2] Install Python(3.5) and PyQt5 and other dependencies<br/>
    i]    pip install pyqt5<br/>
    ii]   pip install numpy<br/>
    iii]  pip install pandas<br/>
    iv]   pip install scipy<br/>
    v]    pip install matplotlib<br/>
3] Inorder to open the application run the following command:<br/>
   python demo.py<br/>

Name of Application : QtPy<br/>

Features:<br/>

Main Tab : First loads the template from "main.ui"<br/>

1] File Menu:<br/>
  a] New         : Creates a new window<br/>
  b] Load        : Helps to load csv file inside tableView (non-editable)<br/>
  c] Save CSV    : Helps to save .csv files<br/>
  d] Save as PNG : Helps to save graph as .png file<br/>
  e] Add Data<br/>
      i]  Add Row    : Add extra row at the end<br/>
      ii] Add Column : Add extra col at the end<br/>
  f] Remove Data <br/>
      i]  Delete Row    : remove the selected row <br/>
      ii] Delete Column : remove the selected col <br/>
  g] Exit : Exits the application <br/>
  
2] Edit Menu:<br/>
  a] Edit Data : Helps to make loaded data editable<br/>
  b] Copy      : Copies data of single cell<br/>
  c] Paste     : Pastes data on single cell<br/>
  d] Cut       : Copy and Remove dara of single cell<br/>
   
3] Plot Menu:<br/>
   
   Plot Tab : First loads the template from "plt.ui"<br/>
   
   a] Plot Data : <br/>
      GUI has:<br/>
      i] 2 comboBox where user is allowed to select 2 attributes from all the available one<br/>
      ii] 4 Buttons : <br/>
          - Scatter Point : Helps in plotting scatter points<br/>
          - Smooth Lines  : Helps in plotting scatter points with smooth lines<br/>
            (It sometimes throws Value Error in some cases)<br/>
          - Line Plot     : Helps in plotting simple line plots<br/>
          - Save as PNG   : Saving the plot as .PNG file<br/>
          
      
