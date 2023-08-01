def get_fb_2000_fields_age_structure() -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     "age_structure.html").expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', 'fb_2000-fields-age_structure_html.md') as target:
        target.write('# Age structure\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)


def get_fb_2000_fields_administrative_divisions() -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     "administrative_divisions.html").expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', 'fb_2000-fields-administrative_divisions_html.md') as target:
        target.write('# administrative divisions\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)


def get_fb_2000_fields(field: str) -> None:
    text_path = Path("~", "Data", "CIA", 
                     "factbook", "factbook_html_zip", "factbook-2000", "fields", 
                     field + '.html').expanduser()
    text = slurp_text_file(text_path)
    source = Source(text, end=len(text))

    selector = Selector('<HR SIZE="3" WIDTH="100%" NOSHADE>')
    title_match = Match('<TITLE>', identifier='title_match')
    title_grab = Grab('</TITLE>', identifier='title_grab')
    p_skip = Match('<p>')
    p_grab = Grab('<p>', identifier='p_grab')
    repeat_p_grab = Repeat([p_grab])
    document = Document([title_match, title_grab, p_skip, repeat_p_grab])
    document.process(source)
    with create_report(experiment, version, 'eda', f'fb_2000-fields-{field:s}_html.md') as target:
        target.write(f'# {field:s}\n\n')
        title_grab.report(target)
        target.write('\n\n')
        p_grab.report(target)
        target.write('\n\n')
        document.report(target)
 
