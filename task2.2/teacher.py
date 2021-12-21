from smart_m3.m3_kp_api import *

if __name__ == '__main__':
    kp = m3_kp_api()
    text = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh 
    euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, 
    quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. 
    Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum 
    dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent 
    luptatum zzril delenit augue duis dolore te feugait nulla facilisi."""

    # Class preparation
    insert_list = [
        Triple(URI('reading_class'), URI('has_text'), Literal(text)),
        Triple(URI('reading_class'), URI('text_pointer'), Literal(0)),
        Triple(URI('reading_class'), URI('text_divider'), Literal(' ')),
    ]
    kp.load_rdf_insert(insert_list)

    # Class start
    input('Waiting for students...\nEnter to start the class:\n')
    insert_list = [
        Triple(URI('reading_class'), URI('reading_queue'), Literal(0)),
        Triple(URI('reading_class'), URI('class_status'), Literal('started')),
    ]
    kp.load_rdf_insert(insert_list)

    # Ctrl+C to end the class
    try:
        while True:
            pass

    except KeyboardInterrupt:
        pass


    print('Goodbye, students!')
    kp.load_query_rdf(Triple(URI('reading_class'), URI('class_status'), None))
    class_over_triple = Triple(URI('reading_class'), URI(
        'class_status'), Literal('finished'))
    kp.load_rdf_update([class_over_triple], kp.result_rdf_query)

    kp.clean_sib()

    kp.leave()
