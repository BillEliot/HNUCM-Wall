<template>
  <div>
    <!-- navbar -->
    <navbar :userBaseInfo="userBaseInfo" />
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>Survival</h1>
                        <p class="subheading">独立游戏</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <div class="container">
        <a-card title="游戏背景">
            <client-only placeholder='Loading'>
                <mavon-editor
                    v-model="background"
                    :subfield="false"
                    defaultOpen="preview"
                    :toolbarsFlag="false"
                    :editable="false"
                    class="editor"
                />
            </client-only>
        </a-card>
        <hr />
        <a-card title="游戏特色">
            <client-only placeholder='Loading'>
                <mavon-editor
                    v-model="content"
                    :subfield="false"
                    defaultOpen="preview"
                    :toolbarsFlag="false"
                    :editable="false"
                    class="editor"
                />
            </client-only>
        </a-card>
    </div>

    <Footer></Footer>

  </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'
import navbar from '~/components/navbar'
import Footer from '~/components/footer'

export default {
  components: {
    navbar,
    Footer
  },
  data() {
    return {
        background:  
`
* 2022年，印第安纳·琼斯教授的手稿重现于世，五大常任理事国召开紧急会议，在菲尼克斯群岛秘密主导成立PTP小组(Possible Turning Point)，进行“TP(Turning Point)”计划。  
* 10年后，包括频率调制理论、诱导立场理论、推进阻饶理论、受控脉冲理论、航迹预算学在内的多种空间理论出现技术爆炸，直属于常任理事国的太空联合舰队成立。  
* 5年后，菲尼克斯群岛依然处于封闭状态，PTP小组仍在运转，“最后的手稿”——生物嫁接理论仍在大量实验中。  
你，太空联合舰队中国属地面部队TP计划特别行动组组长，在例常侦察结束返回菲尼克斯群岛的途中，飞控失灵坠入大海，当醒来时，发现置身荒岛，周遭似真似幻，仿佛一个“幻境”。。。  
`,
        content: 
`
# 采集系统

`
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
      userBaseInfo = response.data
    })

    return {
      userBaseInfo: userBaseInfo
    }
  },
  methods: {

  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
  text-decoration: none
}

.editor {
    z-index: 0;
}
</style>
