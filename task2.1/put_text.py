from smart_m3.m3_kp_api import *

# Just puts the text in the Sib
if __name__ == '__main__':
    kp = m3_kp_api()
    text = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh 
    euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, 
    quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. 
    Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum 
    dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent 
    luptatum zzril delenit augue duis dolore te feugait nulla facilisi."""

    insert_list = [
        Triple(URI('reading_bot'), URI('has_text'), Literal(text))
    ]
    kp.load_rdf_insert(insert_list)
    kp.leave()
