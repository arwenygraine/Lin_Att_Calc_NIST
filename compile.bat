pyinstaller --noconfirm --clean --name="LinAttCalc" --hidden-import="numpy" --hidden-import="pandas" --hidden-import="sqlalchemy" --hidden-import="sqlalchemy.ext.associationproxy" --hidden-import="sqlalchemy.ext.declarative" --hidden-import="sqlalchemy.ext.hybrid" --hidden-import="sqlalchemy.orm" --hidden-import="sqlalchemy.dialects" --hidden-import="six" --exclude-module="mendeleev" --add-data="C:\ProgramData\Miniconda3\Lib\site-packages\mendeleev;mendeleev" --console mainapp.py