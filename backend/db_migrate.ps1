$ENV:FLASK_APP='vapehookah'
$ENV:FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
