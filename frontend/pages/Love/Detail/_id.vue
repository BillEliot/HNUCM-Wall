<template>
    <div>
      <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>（づ￣3￣）づ╭❤～</h1>
                            <p class="subheading">说出来了呢～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="text-center col-md-12">
                    <a-row>
                        <a-col :span="12">
                            <a-avatar :size="64" icon="user" />
                            <div>
                                <a>nickname</a>
                                <p>bio</p>
                            </div>
                        </a-col>
                        <a-col :span="12">
                            <a-avatar :size="64" icon="user" />
                            <div>
                                <a>nickname</a>
                                <p>bio</p>
                            </div>
                        </a-col>
                    </a-row>
                    <hr />
                    <a-card title="对Ta的话">
                        <p>Love ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove ULove U</p>
                    </a-card>
                    <hr />
                    <a-carousel arrows dotsClass="slick-dots slick-thumb">
                        <a slot="customPaging" slot-scope="props">
                            <img :src="getImgUrl(props.i)" />
                        </a>
                        <div v-for="item in 4">
                            <img :src="baseUrl+'abstract0'+item+'.jpg'" />
                        </div>
                    </a-carousel>
                    <hr style="margin-top: 70px" />
                    <a-row>
                        <a-col :span="12">
                            <span>
                            <a-icon type="like-o" style="fontSize: 24px" /> 8
                            </span>
                        </a-col>
                        <a-col :span="12">
                            <span>
                            <a-icon type="message" style="fontSize: 24px" /> 8
                            </span>
                        </a-col>
                    </a-row>
                    <hr />
                    <a-comment>
                        <a-avatar
                            slot="avatar"
                            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
                            alt="Han Solo"
                        />
                        <div slot="content">
                            <a-form-item>
                            <a-textarea :rows="4" @change="handleChange" :value="value" ></a-textarea>
                            </a-form-item>
                            <a-form-item>
                            <a-button
                                htmlType="submit"
                                :loading="submitting"
                                @click="handleSubmit"
                                type="primary"
                            >
                                Add Comment
                            </a-button>
                            </a-form-item>
                        </div>
                    </a-comment>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
const baseUrl = 'https://raw.githubusercontent.com/vueComponent/ant-design-vue/master/components/vc-slick/assets/img/react-slick/'

export default {
  data() {
    return {
        baseUrl
    }
  },
  async asyncData({ $axios }) {

  },
  methods: {
    getImgUrl(i) {
        return `${baseUrl}abstract0${i + 1}.jpg`
    }
  }
}
</script>

<style scoped>
.ant-carousel >>> .slick-dots {
  height: auto
}
.ant-carousel >>> .slick-slide img{
    border: 5px solid #FFF;
    display: block;
    margin: auto;
    max-width: 100%;
}
.ant-carousel >>> .slick-thumb {
  bottom: -45px;
}
.ant-carousel >>> .slick-thumb li {
  width: 60px;
  height: 45px;
}
.ant-carousel >>> .slick-thumb li img {
  width: 100%;
  height: 100%;
  filter: grayscale(100%);
}
.ant-carousel >>> .slick-thumb li.slick-active img{
    filter: grayscale(0%);
}
</style>
