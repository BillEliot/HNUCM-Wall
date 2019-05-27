<template>
    <div class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-2  col-sm-3 col-xs-6">
                    <div class="footer-logo">
                        <div class="footer-logo-text">Eliot Drizzle</div>
                        <p>I love you, but I can't tell you, you know.</p>
                    </div>
                </div>
                <div class="col-md-2 col-sm-3 col-xs-6">
                    <h3>友情链接</h3>
                    <ul class="list-unstyled links">
                        <li>优敏思-UMS</li>
                        <li>UMS-OJ</li>
                        <li>Eliot's Blog</li>
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
                        <li>qq</li>
                        <li>微信</li>
                        <li>qq空间</li>
                        <li>朋友圈</li>
                    </ul>
                </div>
                <div class="col-md-2 col-sm-3 col-xs-6">
                    <h3>联系我</h3>
                    <ul class="list-unstyled links">
                        <li>2017级 中医学院 四班</li>
                        <li>eliotwjz@gmail.com</li>
                        <li>qq: 1161142536</li>
                        <li>wechat: ieliot</li>
                    </ul>
                </div>
            </div>
            <hr />
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
</style>
