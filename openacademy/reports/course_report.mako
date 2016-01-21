<html>
    <head>
        <style type="text/css">${css}</style>
        <title>Course Report</title>
    </head>
    <body>
        <h1>Course Report</h1>
        % for course in objects:
            <h2 style="color:blue">${name}</h2>
            <p><span style="color:green">Sessions:</style>
            <ul>
                % for session in course.session_ids:
                <li>${session.name} - ${session.start_date} to ${session.end_date}</li>
                % endfor
            </ul>
            </p>
            <hr>
        % endfor
    </body>
</html>