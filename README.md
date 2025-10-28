Run :  

python / python3 -m venv venv

source venv/bin/activate (On MacOs)
venv\Scripts\activate (Windows)

pip / pip3 install -r requirements.txt

python / python3 manage.py makemigrations
python / python3 manage.py migrate

python / python3 manage.py runserver

Open Browser -> paste this link -> hit enter
Visit: http://127.0.0.1:8000/



| Role        | Dashboard                   | Permissions           |
| ----------- | --------------------------- | --------------------- |
| Admin       | /tasks/admin_dashboard/     | Manage users & tasks  |
| Teacher     | /tasks/teacher_dashboard/   | Create & assign tasks |
| Student     | /tasks/student_dashboard/   | View & update tasks   |


Author ✌️
Biswajit Bain
GitHub: rbain1218
