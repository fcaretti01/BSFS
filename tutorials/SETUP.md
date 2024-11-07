## Tutorial: Setting Up Python, Visual Studio Code, and GitHub for Your Project

### 1. Download and Install Python

1. **Go to the Python Download Page**:
   - Visit [https://www.python.org/downloads/](https://www.python.org/downloads/).
   
2. **Download the Latest Version**:
   - Click the button for the latest version (it should say something like "Download Python 3.x.x").
   - Make sure to check the box that says **"Add Python to PATH"** before installing.
   
3. **Run the Installer**:
   - Follow the installer prompts to complete the installation.

4. **Verify the Installation**:
   - Open a terminal or command prompt and type:
     ```bash
     python --version
     ```
   - You should see the version number, indicating that Python is installed correctly.

### 2. Install Visual Studio Code (VS Code)

1. **Go to the Visual Studio Code Download Page**:
   - Visit [https://code.visualstudio.com/](https://code.visualstudio.com/).

2. **Download and Install VS Code**:
   - Click on "Download" and choose the version for your operating system (Windows, macOS, or Linux).
   - Follow the installation instructions specific to your OS.

3. **Open Visual Studio Code**:
   - Once installed, open Visual Studio Code.

4. **Install the Python Extension**:
   - In VS Code, go to the **Extensions** view by clicking the square icon on the sidebar or by pressing `Ctrl+Shift+X`.
   - Search for the "Python" extension by Microsoft and click **Install**.

### 3. Set Up Git and GitHub

#### a) Install Git

1. **Download Git**:
   - Go to [https://git-scm.com/](https://git-scm.com/) and download the latest version of Git for your operating system.

2. **Install Git**:
   - Run the installer, following the default options unless you have specific preferences.
   
3. **Verify Git Installation**:
   - Open a terminal or command prompt and type:
     ```bash
     git --version
     ```
   - You should see the Git version number if installed correctly.

#### b) Set Up a GitHub Account

1. **Create a GitHub Account**:
   - Visit [https://github.com/](https://github.com/) and sign up for an account if you don't already have one.


#### c) Clone the Repository to Your Local Directory

1. **Copy the Repository URL**:
   - In your newly created repository on GitHub, click the green **Code** button, and copy the HTTPS link provided.

2. **Open a Terminal and Clone the Repository**:
   - Navigate to the directory where you want to store your project files.
   - In your terminal, type:
     ```bash
     git clone [https://github.com/fcaretti01/BSFS.git]
     ```

3. **Navigate to the Project Directory**:
   - Once cloned, navigate to the project directory:
     ```bash
     cd BSFS
     ```

### 4. Using VS Code with GitHub and Your Project Directory

1. **Open the Project in VS Code**:
   - Open VS Code, then select **File > Open Folder** and navigate to the `BSFS` folder.
   

### 5. Basic Git Commands to Use in Your Project

- **Check Repository Status**:
  ```bash
  git status
  ```

- **Add Files to Commit**:
  ```bash
  git add [file-name]
  ```

- **Commit Changes**:
  ```bash
  git commit -m "Your commit message"
  ```

- **Push to GitHub**:
  ```bash
  git push origin main
  ```

- **Pull Updates from GitHub** (if collaborating with others):
  ```bash
  git pull origin main
  ```

This should set up Python, VS Code, and GitHub for your project so you can start coding and managing version control!