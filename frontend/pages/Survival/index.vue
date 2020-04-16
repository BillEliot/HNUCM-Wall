<template>
  <div>
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="banner">
            <div class="container"></div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>

    <div class="banner-bot">
      <div class="container">
        <h2>欢迎来到 独立游戏 - Survival</h2>
        <p>
          百慕大地区连续发生多起渔民目击怪物事件，作为生物学家的你决定和同事驱船前往百慕大群岛探寻怪物谜象，不料航程遭遇风暴，
          醒来时只有你一人置身于百慕大群岛之上，同事已不知去向，此时你身上带的只有一本荒野求生指南和多年看贝爷节目积攒下的经验......<br>
          生存下去，等待救援 or 意志消沉，葬身荒岛？ 在群岛上展现你的智慧吧！
        </p>
        <a-button type="link">More</a-button>
      </div>
    </div>
    <div class="gallery">
      <div class="contaienr">
        <h3>最新图片</h3>
        <a-carousel arrows>
            <div
                slot="prevArrow"
                slot-scope="props"
                class="custom-slick-arrow"
                style="left: 10px;zIndex: 1"
            >
                <a-icon type="left-circle" />
            </div>
            <div slot="nextArrow" slot-scope="props" class="custom-slick-arrow" style="right: 10px">
                <a-icon type="right-circle" />
            </div>
        </a-carousel>
      </div>
    </div>
    <div class="what-new">
      <div class="container">
        <h3>最近更新</h3>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer.vue'

export default {
    components: {
        navbar,
        Footer
    },
    data() {
        return {
            pictures: [],
            updates: []
        }
    },
    async asyncData({ $axios, redirect }) {
        let userBaseInfo = null

        await $axios.get('getUserBaseInfo')
        .then((response) => {
            userBaseInfo = response.data
            if (userBaseInfo.uid == -1) {
                redirect({ path: '/' })
            }
        })
        
        return {
            userBaseInfo: userBaseInfo
        }
    },
    computed: mapState({
        baseUrl: state => state.baseUrl
    })
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.banner {
    position: relative;
    width: 100%;
    overflow: hidden;
    background-repeat: no-repeat;
    display: block;
    background-image: url(~assets/img/survival/banner.png);
    background-size: cover;
    background-position: center top;
}
.banner .container {
    height: 600px;
}

.banner-bot{
	padding:4em 0;
	text-align:center;
}
.banner-bot h2{
	font-size:4em;
	font-weight:700;
	color:#000;
	margin:0em 0 0.5em 0;
}
.banner-bot p{
	font-size:1.1em;
	font-weight:500;
	color:#000;
	line-height:1.8em;
	margin:0 0 0.5em;
}
.banner-bot p:nth-of-type(2){
	font-weight:100;
	font-size:0.875em;
	margin-bottom:2em;
}
.banner-bot a{
	font-size:2em;
	text-transform:uppercase;
	font-weight:700;
	color:#000;
}

.gallery{
	background:#4fbfa8;
	padding:2em 0;
	text-align:center;
}
.gallery h3{
	font-size:4em;
	font-weight:700;
	color:#fff;
	margin:0em 0 0.5em 0;
}

.what-new{
	padding:2em 0 4em;
	text-align:center;
}
.what-new h3{
	font-size:4em;
	font-weight:700;
	color:#000;
	margin:0.5em 0;
}

.ant-carousel >>> .slick-slide {
  text-align: center;
  height: 160px;
  line-height: 160px;
  background: #364d79;
  overflow: hidden;
}

.ant-carousel >>> .custom-slick-arrow {
  width: 25px;
  height: 25px;
  font-size: 25px;
  color: #fff;
  background-color: rgba(31, 45, 61, 0.11);
  opacity: 0.3;
}
.ant-carousel >>> .custom-slick-arrow:before {
  display: none;
}
.ant-carousel >>> .custom-slick-arrow:hover {
  opacity: 0.5;
}

.ant-carousel >>> .slick-slide h3 {
  color: #fff;
}
</style>
