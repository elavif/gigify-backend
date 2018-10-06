

def get_page():
	return """
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sightengine demo - Python and Flask</title>
  <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/app.css') }}">
</head>

<body>
<header class="navbar">
  <form action="/image_upload" method="post" enctype="multipart/form-data" >
      <span class="btn btn-default btn-file">
        Browse <input type="file" name="image">
      </span>

    <input type="submit" value="Upload your image" class="btn btn-primary">
  </form>

</header>

</body>
</html>
	"""


def comment_page():
	return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>


.commentcontainer {
    border: 2px solid #dedede;
    background-color: #f1f1f1;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

.darker {
    border-color: #ccc;
    background-color: #ddd;
}

.commentcontainer::after {
    content: "";
    clear: both;
    display: table;
}

.commentcontainer img {
    max-height: 500px;
    max-width: 700px;
    width: auto;
    margin-right: 20px;
}


.time-right {
    float: right;
    color: #aaa;
}

.time-left {
    float: left;
    color: #999;
}
</style>
</head>
<body>

<h2>Chat Messages</h2>
<div style="margin: 0 auto; max-width: 800px; padding: 0 20px">
<!-- NOTE TO BURAK : BELOW IS WHAT U GET FROM gig's details attribute -->
\n\t<div class=\"commentcontainer darker\">\n\t  <b>Burak Icel uploaded a photo:</b><br>\t\n\t  <img src=\"http://localhost:5000/images/587f473e-eec1-48de-a9b6-41af2820c469.png\"><br>\n\t  <span class=\"time-left\">2018-10-06 13:05:26.839433</span>\n\t</div>\n\t</html>


	"""


def comment_box():
  return """
  <!-- begin wwww.htmlcommentbox.com -->
 <div id="HCB_comment_box"></div>
 <link rel="stylesheet" type="text/css" href="//www.htmlcommentbox.com/static/skins/bootstrap/twitter-bootstrap.css?v=0" />
 <script type="text/javascript" id="hcb"> /*<!--*/ if(!window.hcb_user){hcb_user={};} (function(){var s=document.createElement("script"), l=hcb_user.PAGE || (""+window.location).replace(/'/g,"%27"), h="//www.htmlcommentbox.com";s.setAttribute("type","text/javascript");s.setAttribute("src", h+"/jread?page="+encodeURIComponent(l).replace("+","%2B")+"&opts=16862&num=10&ts=1538858838337");if (typeof s!="undefined") document.getElementsByTagName("head")[0].appendChild(s);})(); /*-->*/ </script>
<!-- end www.htmlcommentbox.com --> """















