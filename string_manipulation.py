def remove_obstacles(username):
    username = username.replace('[',"")
    username = username.replace(']',"")
    username = username.replace('(',"")
    username = username.replace(')',"")
    username = username.replace('\'',"" )
    username = username.replace(',',"")
    return username 