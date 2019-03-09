# fsf_2019_screening_task2

Steps to run this application :<br />
1] Download and extract all the files in a folder<br />
2] Install Python(3.5) and PyQt5 and other dependencies<br />
    &nbsp;&nbsp;&nbsp;i]    pip install pyqt5<br/>
    &nbsp;&nbsp;&nbsp;ii]   pip install numpy<br/>
    &nbsp;&nbsp;&nbsp;iii]  pip install pandas<br/>
    &nbsp;&nbsp;&nbsp;iv]   pip install scipy<br/>
    &nbsp;&nbsp;&nbsp;v]    pip install matplotlib<br />
3] Inorder to open the application run the following command:<br/>
   python demo.py<br  />

Name of Application : QtPy<br />

Features:<br />

Main Tab : First loads the template from "main.ui"<br />

1] File Menu:<br />
  &nbsp;&nbsp;&nbsp;a] New         : Creates a new window<br/>
  &nbsp;&nbsp;&nbsp;b] Load        : Helps to load csv file inside tableView (non-editable)<br/>
  &nbsp;&nbsp;&nbsp;c] Save CSV    : Helps to save .csv files<br/>
  &nbsp;&nbsp;&nbsp;d] Save as PNG : Helps to save graph as .png file<br/>
  &nbsp;&nbsp;&nbsp;e] Add Data<br/>
      &nbsp;&nbsp;&nbsp;i]  Add Row    : Add extra row at the end<br/>
      &nbsp;&nbsp;&nbsp;ii] Add Column : Add extra col at the end<br/>
  &nbsp;&nbsp;&nbsp;f] Remove Data <br/>
      &nbsp;&nbsp;&nbsp;i]  Delete Row    : remove the selected row <br/>
      &nbsp;&nbsp;&nbsp;ii] Delete Column : remove the selected col <br/>
  &nbsp;&nbsp;&nbsp;g] Exit : Exits the application <br />
  
2] Edit Menu:<br />
  &nbsp;&nbsp;&nbsp;a] Edit Data : Helps to make loaded data editable<br/>
  &nbsp;&nbsp;&nbsp;b] Copy      : Copies data of single cell<br/>
  &nbsp;&nbsp;&nbsp;c] Paste     : Pastes data on single cell<br/>
  &nbsp;&nbsp;&nbsp;d] Cut       : Copy and Remove dara of single cell<br/>
   
3] Plot Menu:<br />
   
   Plot Tab : First loads the template from "plt.ui"<br />
   
   a] Plot Data : <br />
      GUI has:<br/>
      i] 2 comboBox where user is allowed to select 2 attributes from all the available one<br/>
      ii] 4 Buttons : <br/>
          &nbsp;&nbsp;&nbsp;- Scatter Point : Helps in plotting scatter points<br/>
          &nbsp;&nbsp;&nbsp;- Smooth Lines  : Helps in plotting scatter points with smooth lines<br/>
            (It sometimes throws Value Error in some cases)<br/>
          &nbsp;&nbsp;&nbsp;- Line Plot     : Helps in plotting simple line plots<br/>
          &nbsp;&nbsp;&nbsp;- Save as PNG   : Saving the plot as .PNG file<br/>
          
      
