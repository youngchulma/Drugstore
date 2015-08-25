__author__ = 'Randy'

# coding=utf-8
import threading
import urllib
import re


def request_html(url_str):
    page = urllib.urlopen(url_str)
    content = page.read()
    page.close()

    return content


def reg_link(content_str):
    # reg_exp = r'<a\href=\"(ed2k?://[^"]+)\"\s*>([^<]+)<\/a>'
    # reg_exp = r'ed2k?://[^"]*/'
    reg_exp = r'"(ed2k?://[^"]+)"'
    reg_content = re.compile(reg_exp)
    down_link = re.findall(reg_content, content_str)

    if len(down_link) > 0:
        # return the first item from list
        return down_link[0]


def get_pdf_link(start_idx, end_idx):
    pdf_link_list = []
    url_str = "http://bt8.nl/bookinfo.php?%s"

    for idx in range(start_idx, end_idx):
        url_param = urllib.urlencode({'id': idx})
        pdf_link = reg_link(request_html(url_str % url_param))

        # append the link to list
        pdf_link_list.append(pdf_link)

        print pdf_link
        print len(pdf_link_list)

    return pdf_link_list


def save_pdf_file(thread_idx, start_idx, end_idx):
    pdf_down_file = "download" + str(thread_idx) + ".txt"
    pdf_link_file = open(pdf_down_file, "a+")

    pdf_link_list = get_pdf_link(start_idx, end_idx)

    for idx in range(start_idx-1, end_idx-1):
        pdf_link_file.write(pdf_link_list.__getitem__(idx).__str__()+'\n')

    pdf_link_file.flush()
    pdf_link_file.close()

    return 0


def main():
    pdf_count = 12994
    base_count = 1000

    pdf_thread_list = []

    mod_count = pdf_count % base_count
    quo_count = pdf_count / base_count

    if mod_count != 0:
        quo_count += 1

    count = 1
    str_idx = 1
    end_idx = base_count
    for i in range(1, quo_count+1):
        print i, str_idx, end_idx

        if count != quo_count-1:
            str_idx += base_count
            end_idx += base_count
        else:
            str_idx += base_count
            end_idx += mod_count

        count += 1

        pdf_thread = threading.Thread(target=save_pdf_file, args=(i,str_idx,end_idx))
        pdf_thread.start()
        pdf_thread_list.append(pdf_thread)

    for idx in range(1,quo_count+1):
        pdf_thread = pdf_thread_list[idx]
        pdf_thread.join()


if __name__ == '__main__':
    main()
