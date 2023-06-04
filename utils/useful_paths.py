
CONTAINER = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body {
            margin-left: 23%%;
            margin-right: 23%%;
            font-family: System-ui;
        }

        .body-lg {
            line-height: 1.5;
            font-family: sans-serif;
            font-size: 16px;
            line-height: 24px;
            color: rgb(18, 18, 18);
        }

        header>div>div>ul {
            display: flex;
            flex-direction: row;
            margin-left: 0;
            padding-left: 0;
        }

        header>div>div>ul>li {
            list-style-type: none;
            margin-right: 5px;
            padding: 0;
        }

        header>div>div>ul>li>span>a {
            margin-left: 5px;
            text-decoration: none;
            font-weight: 600;
            color: black;
            font-size: 16px;
            line-height: 24px;
        }

        img {
            object-fit: fill;
            width: 100%%;
            height: auto;
            padding: 0;
            margin: 0;
        }

        figure {
            padding: 0;
            margin: 0;
        }

        h1 {
            font-size: 48px;
            line-height: 57.6px;
            color: rgb(18, 18, 18);
            font-weight: 400;
        }

        li > span {
            margin-right: 10px;
        }

        header>div>div>ul>li>span>a:hover {
            color: rgb(31, 143, 191);
        }
    </style>
</head>

<body>
    %(content)s
</body>

</html>
'''

PROXIES = {
    "http": "http://318a06daae614a4bae88c743d2109310:@proxy.crawlera.com:8011/",
    "https": "http://318a06daae614a4bae88c743d2109310:@proxy.crawlera.com:8011/",
}

VERIFY = '/usr/local/share/ca-certificates/zyte-smartproxy-ca.crt'
