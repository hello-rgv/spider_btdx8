""" Python 练习 采集比特大熊 (http://www.btdx8.com) 影片数据

Date: 2018-1-5
Author: Mr Bean

Python version : 3.6
Module         : requests
IDE            : PyCharm 2017.3
OS             : win10

"""


import requests
import re


def get_movie_type_list():
    """ 网站影片类型列表
     返回:
        Tuple
    """
    type_list = (
        # 动作片 0
        "http://www.btdx8.com/category/dongzuo",
        # 犯罪片 1
        "http://www.btdx8.com/category/fanzui",
        # 科幻片 2
        "http://www.btdx8.com/category/kehuan",
        # 悬疑片 3
        "http://www.btdx8.com/category/xuanyi",
        # 战争片 4
        "http://www.btdx8.com/category/zhanzheng",
        # 爱情片 5
        "http://www.btdx8.com/category/aiqing",
        # 恐怖片 6
        "http://www.btdx8.com/category/kongbu",
        # 灾难片 7
        "http://www.btdx8.com/category/zainan",
        # 喜剧片 8
        "http://www.btdx8.com/category/xiju",
        # 动画片 9
        "http://www.btdx8.com/category/donghua",
        # 剧情片 10
        "http://www.btdx8.com/category/juqing",
        # 纪录片 11
        "http://www.btdx8.com/category/jilupian"
    )
    return type_list


def clear_href(content):
    """
    清除抓取html片段的 a 链接
    参数:
        content
            需要清除 a 链接的html源代码
    返回:
        str
    """
    regex_href = r'href'
    is_href = re.findall(regex_href, content)
    if is_href:
        for n in range(len(is_href)):
            result_text = re.subn(r'<a\shref=.*?>', "", content)
            result_text = re.subn(r'</a>', "", result_text[0])
        return result_text[0]
    else:
        return content


def get_page_last_num(movie_type_list_url):
    """
    抓取影片列表最后页数

    参数:
        movie_type_list_url
        影片某个类型的列表页面 url
    返回:
        last_num : int
        某个类型的影片列表最后的页数

    """
    rsp = requests.get(movie_type_list_url)
    rsp_text = rsp.text

    regex_page_num_html = r'<div\sclass=[\s\S]wp-pagenavi[\s\S]>(.*?)</div>'
    page_num_html = re.findall(regex_page_num_html, rsp_text)[0]

    regex_last_num = r'class="last"\shref=".*?/page/(.*?)"'
    last_num = re.findall(regex_last_num, page_num_html)[0]

    return int(last_num)


def get_movie_list_info(url):
    """
    抓取影片列表信息
    参数:
        url
        影片某个类型的列表页面 url
    返回:
        dict
    """
    result_info = []
    rsp = requests.get(url)
    rsp_content = rsp.text

    regex_movie_list_html = r'<div\sid="post-.*?>(.*?)</div>'
    movie_list_html = re.findall(regex_movie_list_html, rsp_content)

    for n in range(len(movie_list_html)):
        regex_movie_href = r'<a\sclass="entry-thumb lazyload"\shref="(.*?)"\stitle="(.*?)"'
        movie_href = re.findall(regex_movie_href, movie_list_html[n])
        result_info.append(movie_href)

    return result_info


def get_movie_info(movie_page_url):
    """ 采集影片信息

        参数:
            movie_page_url
            影片详情页面地址
        返回:
            dict
    """

    movie_info = {}

    rsp = requests.get(movie_page_url)
    rsp_content = rsp.text

    # 影片 post-id
    movie_info['id'] = get_movie_post_id(rsp_content)

    # 影片名称
    regex_movie_name = r'<span\sclass="current">(.*?)</span>'
    movie_name = re.findall(regex_movie_name, rsp_content)[0]
    movie_info["name"] = movie_name
    # 影片封面图片
    regex_movie_image = r'<div\sid="poster_src"><img\ssrc="(.*?)"'
    movie_image = re.findall(regex_movie_image, rsp_content)[0]
    movie_info["image"] = movie_image
    # 影片采集日期
    regex_movie_collection_date = r'<span\sclass="meta-date"\stitle=".*?">.*?：(.*?)</span>'
    movie_collection_date = re.findall(regex_movie_collection_date, rsp_content)[0]
    movie_info["collection_date"] = movie_collection_date
    # 抓取影片 导演、编剧、演员等html片段
    regex_movie_info_html = r'<div\sid="movie_info">(.*?)</div>'
    movie_info_html = re.findall(regex_movie_info_html, rsp_content)[0]
    # 影片导演
    regex_director_html = r'导演:(.*?)<br\s/>'
    movie_director_html = re.findall(regex_director_html, movie_info_html)[0]
    movie_director = clear_href(movie_director_html)
    movie_info["director"] = movie_director
    # 影片编剧
    regex_screenwriter_html = r'编剧:(.*?)<br\s/>'
    movie_screenwriter_html = re.findall(regex_screenwriter_html, movie_info_html)
    if movie_screenwriter_html:
        movie_screenwriter = clear_href(movie_screenwriter_html[0])
        movie_info["screenwriter"] = movie_screenwriter
    else:
        movie_info["screenwriter"] = ""
    # 影片演员
    regex_performers_html = r'主演:(.*?)<br\s/>'
    movie_performers_html = re.findall(regex_performers_html, movie_info_html)[0]
    movie_performers = clear_href(movie_performers_html)
    movie_info["performers"] = movie_performers
    # 影片类型
    regex_type_html = r'类型:(.*?)<br\s/>'
    movie_type_html = re.findall(regex_type_html, movie_info_html)[0]
    movie_type = clear_href(movie_type_html)
    movie_info["type"] = movie_type
    # 制片国家
    regex_country_html = r'地区:(.*?)<br\s/>'
    movie_country_html = re.findall(regex_country_html, movie_info_html)[0]
    movie_country = clear_href(movie_country_html)
    movie_info["country"] = movie_country
    # 影片语言
    regex_language_html = r'语言:(.*?)<br\s/>'
    movie_language_html = re.findall(regex_language_html, movie_info_html)[0]
    movie_language = clear_href(movie_language_html)
    movie_info["language"] = movie_language
    # 影片上映日期
    regex_release_date_html = r'上映日期:(.*?)<br\s/>'
    movie_release_date_html = re.findall(regex_release_date_html, movie_info_html)

    if movie_release_date_html:
        movie_release_date_html = movie_release_date_html
    else:
        regex_release_date_html = r'上映日期:(.*?)$'
        movie_release_date_html = re.findall(regex_release_date_html, movie_info_html)

    if movie_release_date_html:
        movie_release_date = clear_href(movie_release_date_html[0])
        movie_release_date = re.subn(r'\(.*?\)', "", movie_release_date)[0]
        movie_info["release_date"] = movie_release_date
    else:
        movie_info["release_date"] = ""
    # 影片时间
    regex_time_length_html = r'片长:(.*?)(?:<br\s/>|</div>|$)'
    movie_time_length_html = re.findall(regex_time_length_html, movie_info_html)
    if movie_time_length_html:
        movie_time_length = movie_time_length_html[0]
        movie_info["time_length"] = movie_time_length
    else:
        movie_info["time_length"] = ""
    # 影片剧情简介
    regex_description_html = r'<div\sid="movie_description">(.*?)</div>'
    movie_description = re.findall(regex_description_html, rsp_content)[0]
    movie_info["description"] = movie_description
    # 影片截图
    regex_screenshot_html = r'<ul\sclass="moviepic-img">(.*?)</ul>'
    movie_screenshot_html = re.findall(regex_screenshot_html, rsp_content)[0]
    regex_screenshot = r'<img\s.*?src="(.*?)"'
    movie_screenshot = re.findall(regex_screenshot, movie_screenshot_html)
    movie_info["screenshot"] = movie_screenshot

    return movie_info


def get_movie_post_id(html_code):
    """ 抓取影片的 post-id (post-id是该网站影片的唯一标识, 进入下载页面的时候需要该表示加入cookies)
    参数:
        html_code
            影片详情页面html源码
    返回:
        string
    """
    regex_post_id = r'<div\sid="post-(.*?)"\sclass='
    movie_post_id = re.findall(regex_post_id, html_code)
    return movie_post_id[0]


def get_movie_download(html_code):
    """ 抓取影片详情页面的下载页面链接地址，因为链接地址每次刷新页面都会自动改变，所以得"现做现吃"
    parameter:
        html_code: 影片详情页面html源码
    return: 以列表形式的下载页面链接 (tuple)
    """
    regex_movie_download_html = r'<div\sid="zdownload"><a\shref="(.*?)"[\s\S]*?><span>(.*?)</span>(.*?)</a>'
    movie_download = re.findall(regex_movie_download_html, html_code)
    return movie_download


def get_movie_down_page(down_url, movie_post_id):

    """ 获取影片下载页面源代码
    参数:
        down_url
        影片详情页面的下载地址

        movie_post_id
        影片id

    返回:
        list

    """
    btpc = 'btpc_' + movie_post_id
    cookies = {}
    cookies[btpc] = movie_post_id
    respons = requests.post(down_url, cookies=cookies)
    respons_text = respons.text
    return respons_text


def get_movie_down_href(html_code, movie_post_id):
    """ 抓取影片种子下载链接
    参数:
        html_code
            影片下载页面html源代码

        movie_post_id
            影片id

    返回:
        string
    """
    regex = r'fc:\s"([^"].*?)"'
    reg = re.compile(regex)
    fc = reg.findall(html_code)
    result_data = {'file_id': movie_post_id, 'fc': fc[0]}
    # 生成下载链接的地址
    movie_down_url = 'http://www.btdx8.com/calldown/calldown.php'
    rsp = requests.post(movie_down_url, result_data)
    rsp_json_content = rsp.json()
    return rsp_json_content


def down_movie_file(file_name, down_href, headers_referer):
    """ 下载影片种子文件
    参数:
        file_name
            下载种子文件名

        down_href
            种子文件下载地址

        headers_referer
            下载文件时发送的请求头Referer参数

    返回:
        bool
            下载成功 True, 反之 False

    """
    headers = {'Referer': headers_referer}
    rsp = requests.get(down_href, headers=headers)
    headers_content_type = rsp.headers['Content-Type']
    if headers_content_type != 'text/html; charset=utf-8':
        with open(file_name, "wb") as movie_file:
            movie_file.write(rsp.content)
        return True
    else:
        print('下载种子文件失败，请在浏览器下查看种子文件是否能够正确下载.')
        return False


def main_test():

    """ 测试抓取某个类型的电影列表信息 """

    # 获取影片类型列表

    # movie_type_list = get_movie_type_list()
    # # 获取某个类型电影列表的总页数
    # page_last_num = get_page_last_num(movie_type_list[0])
    # print('共 {num} 页'.format(num=page_last_num))
    # n = 0
    # for page_num in range(10):
    #     # 拼接影片列表链接
    #     movie_list_url = movie_type_list[0] + "/page/" + str(page_num + 1)
    #     # 获取影片信息
    #     movie_list_info = get_movie_list_info(movie_list_url)
    #     for l in movie_list_info:
    #         n += 1
    #         for t in l:
    #             print("{rowId}. {name} , {href}".format(rowId=n, name=t[1], href=t[0]))
    #             print('{:-<150}'.format('-'))

    # =======================================================================================


    # 测试抓取影片详细信息

    # movie_info = get_movie_info('http://www.btdx8.com/torrent/ssw_2017-2.html')
    # for k in movie_info:
    #     print(k, ':', movie_info[k])

    # =======================================================================================

    # 测试抓取影片详情页面的下载页面链接地址

    # rsp = requests.get('http://www.btdx8.com/torrent/ssw_2017-2.html')
    # rsp_text = rsp.text
    # down_href = get_movie_download(rsp_text)
    # print(down_href)

    # =======================================================================================

    # 测试抓取影片下载页面并下载影片种子文件
    # url = 'http://www.btdx8.com/torrent/jqzx_2017.html'
    # rsp = requests.get(url)
    # rsp_text = rsp.text
    # # 影片详情页面的下载地址
    # movie_down_info = get_movie_download(rsp_text)
    #
    # # 影片 id
    # post_id = get_movie_post_id(rsp_text)
    #
    # # 影片名称
    # movie_name = movie_down_info[0][2]
    #
    # # 影片下载页面链接地址
    # movie_href = movie_down_info[0][0]
    #
    # # 获取下载页面html源码
    # movie_down_page_code = get_movie_down_page(movie_href, post_id)
    #
    # # 种子文件下载链接
    # movie_down_href = get_movie_down_href(movie_down_page_code, post_id)
    #
    # # 下载种子文件
    # if not down_movie_file(movie_name, movie_down_href['down'], movie_href):
    #     print('下载失败的影片地址: ', url)
    # =======================================================================================


main_test()
