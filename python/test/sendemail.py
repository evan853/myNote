# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


if __name__=="__main__":
    # 输入Email地址和口令:
    from_addr = ""
    password = ""
    # 输入SMTP服务器地址:
    smtp_server = ""
    # 输入收件人地址:
    to_addr = ""

    msg = MIMEMultipart('alternative')

    #msg = MIMEText(u'<html><body><h1>Hello</h1>' +
    #u'<p>send by <a href="http://www.baidu.com">百度</a>...</p>' +
    #u'</body></html>', 'html', 'utf-8')
    msg['From'] = _format_addr(u'服务器管理员 <%s>' % from_addr)
    msg['To'] = _format_addr(u'evan <%s>' % to_addr)
    msg['Subject'] = Header(u'出问题了!!', 'utf-8').encode()
    # 邮件正文是MIMEText:
    msg.attach(MIMEText(u'我是普通文本', 'plain', 'utf-8'))
    msg.attach(MIMEText(u'<html><body><h1>NBA赛事</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open(u'H:/垃圾图片/142946217.jpg', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'jpg', filename=u'142946217.jpg')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=u'142946217.jpg')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server,587) # SMTP协议默认端口是25
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
