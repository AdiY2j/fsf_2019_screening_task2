# fsf_2019_screening_task2

Steps to run this application :
1] Download and extract all the files in a folder
2] Install Python(3.5) and PyQt5 and other dependencies
    i]    pip install pyqt5
    ii]   pip install numpy
    iii]  pip install pandas
    iv]   pip install scipy
    v]    pip install matplotlib
3] Inorder to open the application run the following command:
   python demo.py

Name of Application : QtPy

Features:

Main Tab : First loads the template from "main.ui"

1] File Menu:
  a] New         : Creates a new window
  b] Load        : Helps to load csv file inside tableView (non-editable)
  c] Save CSV    : Helps to save .csv files
  d] Save as PNG : Helps to save graph as .png file
  e] Add Data
      i]  Add Row    : Add extra row at the end
      ii] Add Column : Add extra col at the end
  f] Remove Data 
      i]  Delete Row    : remove the selected row 
      ii] Delete Column : remove the selected col
  g] Exit : Exits the application
  
2] Edit Menu:
  a] Edit Data : Helps to make loaded data editable
  b] Copy      : Copies data of single cell
  c] Paste     : Pastes data on single cell
  d] Cut       : Copy and Remove dara of single cell
  
3] Plot Menu:
   
   Plot Tab : First loads the template from "plt.ui"
   
   a] Plot Data : 
      GUI has:
      i] 2 comboBox where user is allowed to select 2 attributes from all the available one
      ii] 4 Buttons : 
          - Scatter Point : Helps in plotting scatter points
          - Smooth Lines  : Helps in plotting scatter points with smooth lines
            (It sometimes throws Value Error in some cases)
          - Line Plot     : Helps in plotting simple line plots
          - Save as PNG   : Saving the plot as .PNG file
          
      
