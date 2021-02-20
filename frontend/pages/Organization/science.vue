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
                            <h1>大学生科学技术协会</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12 text-center">
                    <a-tabs type="card">
                        <a-tab-pane tab="组织介绍" key="1">
                            <p>大学生科学技术协会是由校团委、科技处共同指导的全校性学生学术科技组织，于2012年9月29日成立，是校级四大学生组织之一。通过组织我校同学参加“挑战杯”、“互联网+”、“天堰杯”、“远志杯”等大学生课外学术科技作品竞赛，大学生创新创业竞赛以及组织杏林讲坛、助研计划等活动。在丰富同学们课余生活的同时，营造我校科技创新氛围。</p>
                        </a-tab-pane>
                        <a-tab-pane tab="部门设置" key="2">
                            <a-tabs type="card">
                                <a-tab-pane tab="办公室" key="1">
                                    <p>办公室负责科协内部相关文件的起草，整理及收集各项比赛活动的策划作品、获奖情况及总结；科协内信息的上传与下达及科协办公室的管理；部长级例会和各二级学院科技部部长例会的会议记录；大学生科协所有计费的支配与管理等。在负责相关文件的起草时，我们怀揣着一份担当。在上下传达信息时，我们手握着一份责任。在管理经费的支配时，我们秉持着一份公正。</p>
                                </a-tab-pane>
                                <a-tab-pane tab="组织部" key="2">
                                    <p>组织部主要负责大科协会员及人事管理、成员整体素质与能力的提升、各项工作的监督考核以及内部活动，组织和策划大科协举办的各项活动，并带领大学生科协会员参加校内及校外活动。细腻、真挚。工作时一本正经，闲暇时一笑生花。</p>
                                </a-tab-pane>
                                <a-tab-pane tab="新闻网络部" key="3">
                                    <a-tabs type="card">
                                        <a-tab-pane tab="部门介绍" key="1">
                                            <p>大科协的“技术担当”，下设两组，分工合作，井然有序：宣传组负责大科协宣传栏的海报绘制、公示发表以及各个讲座、活动的黑板报绘制；网络组负责各大活动所需的电子海报、PPT和视频的制作。我们用网络传播校园的风采，我们用彩笔构图学校的蓝图，我们用媒体传达湖中大的每一个瞬间，我们深沉的爱着我们的每一份工作。好看的皮囊千篇一律，有趣的灵魂，新网人也。</p>
                                        </a-tab-pane>
                                        <a-tab-pane tab="远志传媒" key="2">
                                            <p>新媒体工作室，主要负责大科协微信公众号的图文排版与推送、管理官方QQ、进行活动宣传，拍摄。分为两组：排版与摄影组；新闻组（负责活动记录，写新闻稿，文字编辑)。这里是幕后的英雄，这里是科协对外开放与交流的窗口，这里是科协信息汇集与发布的源泉。我们在这里等你。</p>
                                        </a-tab-pane>
                                    </a-tabs>
                                </a-tab-pane>
                                <a-tab-pane tab="科技创新部" key="4">
                                    <p>主要负责组织“挑战杯”、“ 远志杯”、“天堰杯" 等大型科技创新类比赛和知识产权竞赛。同时负责校内师生间“助研计划”的开展，致力于筑起教师与学生在科研上沟通的桥梁。在这里你不仅可以接触到全校最前沿的科研资讯，还可以亲自投身于各科研比赛的筹备，在对科研的兴趣中增加自己的能力。还在犹豫什么，科创就是你的选择！</p>
                                </a-tab-pane>
                                <a-tab-pane tab="创业实践部" key="5">
                                    <p>主要负责协办各种创新创业及实践挑战类比赛，将学生的创业作品推至更广阔的舞台。同时会举办创业培训班，对创业团队进行创业素质、法律意识等创业基本技能的培训。让学生对创业有着更为深入的了解。如果你也有个创业实践梦，这里就是舞台。</p>
                                </a-tab-pane>
                                <a-tab-pane tab="信息调研部" key="6">
                                    <p>大科协的数据中心，负责大科协信息的收集，整理与分析，做好对我校师生科研成果以及校内外相关组织之间交流工作的收集与总结，信息，我们包罗万象;调研，我们事无巨细。问卷调查，对外交流，我们担任着大科协的眼和耳，我们让科协感知世界。快来pick信调吧！</p>
                                </a-tab-pane>
                                <a-tab-pane tab="科普部" key="7">
                                    <a-tabs type="card">
                                        <a-tab-pane tab="部门介绍" key="1">
                                            <p>负责全校科普活动的制定并实施，如科普融生活、热点科普话题征文、举办杏林讲堂等。这里有一群有趣的求知灵魂，这里是知识的海洋、真理的天堂和智慧的聚集地。让我们一起感受科普的魅力！</p>
                                        </a-tab-pane>
                                        <a-tab-pane tab="讲解队" key="2">
                                            <p>负责两馆一园的讲解活动；常在中药标本馆、人体科学馆及药植园进行日常训练，经常需要接待外来的参观人员，包括领导、外国人士、中小学生等。左手轻点，是人体标本馆展现的人体奥秘。右手一指，是中药标本馆背后中药发展源远流长的历史；挺直的腰身，亲切的微笑，你喜欢的样子，在讲解队都可以实现！</p>
                                        </a-tab-pane>
                                    </a-tabs>
                                </a-tab-pane>
                            </a-tabs>
                        </a-tab-pane>
                    </a-tabs>
                </div>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'
import { mapState } from 'vuex'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    return {
        userBaseInfo: userBaseInfo,
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
    text-decoration: none;
}
</style>
