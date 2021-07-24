<template>
    <div class="footer">
        <div class="container">
            <div class="row">
                <div class="text-center">
                    <div class="col-md-2  col-sm-3 col-xs-6">
                        <div class="footer-logo">
                            <div class="footer-logo-text">Eliot Drizzle</div>
                            <p>似水, 吾友</p>
                            <p>Be water, my friend</p>
                            <p>水のように, 私の友達</p>
                            <p>물처럼 내 친구</p>
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-3 col-xs-6">
                        <h3>友情链接</h3>
                        <ul class="list-unstyled links">
                            <li><a target="_blank" href="https://billeliot.github.io">Eliot's Blog</a></li>
                            <li><a target="_blank" href="https://www.medai.vip">中医术语中英对照查询系统</a></li>
                            <li><a target="_blank" href="http://jwmis.hnucm.edu.cn">湖南中医药大学教务管理系统</a></li>
                            <li><a target="_blank" href="https://www.hnucm.edu.cn">湖南中医药大学</a></li>
                            <li><a target="_blank" href="https://www.sdutcm.edu.cn">山东中医药大学</a></li>
                        </ul>
                    </div>
                    <div class="col-md-2 col-sm-3 col-xs-6">
                        <h3>HNUCM-Wall</h3>
                        <ul class="list-unstyled links">
                            <li>关于墙墙</li>
                        </ul>
                    </div>
                    <div class="col-md-2 col-sm-3 col-xs-6">
                        <h3>分享</h3>
                        <ul class="list-unstyled links">
                            <li>
                                <a target='_blank' href="http://connect.qq.com/widget/shareqq/index.html?url=https://hnucmwall.top&title=湖南中医药大学校园墙&desc=湖南中医药大学校园墙&summary=湖南中医药大学校园墙">qq</a>
                            </li>
                            <li>
                                <a target='_blank' href="http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=https://hnucmwall.top/&title=湖南中医药大学校园墙&desc=湖南中医药大学校园墙&summary=湖南中医药大学校园墙">qq空间</a>
                            </li>
                        </ul>
                    </div>
                    <div class="col-md-2 col-sm-3 col-xs-6">
                        <h3>联系我</h3>
                        <ul class="list-unstyled links">
                            <li>eliotwjz@gmail.com</li>
                            <li>wechat: EliotDrizzle</li>
                        </ul>
                    </div>
                </div>
            </div>
            <hr />
            <div class="text-center">
                <span class="copyright">© 2019~2021 hnucmwall.top 版权所有 ICP证：<a href="https://beian.miit.gov.cn" target="_blank">冀ICP备20008221号</a></span>
                <br />
                <span>
                    <img src="~assets/img/copyright.png">
                    <a href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=37010102000760" target="_blank">鲁公网安备 37010102000760号</a>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
    }
  }
}
</script>

<style>
.footer{
    margin-top: 200px;
    padding: 60px 0;
    background-color: #1A252E;
    font-family: 'Source Sans Pro', sans-serif;
}

.footer a {
    text-decoration: none;
}

.footer-logo .footer-logo-text {
    color: #fff;
    font-family: "Oleo Script",cursive;
    font-size: 25px;
    font-weight: 400;
    margin-bottom: 10px;
}

.footer-logo p{
    color: #eee;
    font-weight: 400; 
    font-size: 13px
}

.footer-logo img{
    width: 95px;
    margin-bottom: 15px;
}

.links li i{
    margin-right: 5px; 
    font-size: 14px;
}

.links li{
    cursor: pointer;
    color: #94a5b4; 
    font-weight: 600;
    margin-bottom: 9px;
}

.links li:hover{
    color: #fff;
}

.footer h3 {
    color: #fff;
    font-size: 20px;
    font-weight: 400;
    margin-bottom: 15px;
    margin-top: 0;
}

.footer hr{
    border-color: #393939;
}

.copyright {
    color: white;
}
</style>
