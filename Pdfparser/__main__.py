__author__ = 'Randy'

# coding=utf-8
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


def save_pdf_file():
    pdf_link_file = open("download.txt", "a+")

    start_idx = 1
    # end_idx = 12994
    end_idx = 11

    pdf_link_list = get_pdf_link(start_idx, end_idx)

    for idx in range(start_idx-1, end_idx-1):
        pdf_link_file.write(pdf_link_list.__getitem__(idx).__str__()+'\n')

    pdf_link_file.flush()
    pdf_link_file.close()

    return 0


if __name__ == '__main__':
    save_pdf_file()
