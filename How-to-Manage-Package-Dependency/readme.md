# How to Manage Package Dependency with Conda Virtual Environment

1. Please install anaconda
2. Add your anaconda path to environment path (ex :C:\Users\Hanif\anaconda3\Scripts)
3. Test your conda cmd in powershell 

```
conda --version
```

4. Create your virtual enviroment

```
conda create -n modelenv python=3.10 -y
```

5. Initial conda cmd

```
conda init powershell
```
5. Activate virtual enviroment

```
conda activate modelenv
```

6. Python install dependency packages

```
pip install -r requirements.txt
```






