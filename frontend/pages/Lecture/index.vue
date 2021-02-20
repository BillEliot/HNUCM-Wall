<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="嘉宾信息"
            placement="bottom"
            height=512
            @close="visible = false"
            :visible="visible"
        >
            <mavon-editor
                v-model="lecturerInfo"
                :subfield="false"
                defaultOpen="preview"
                :toolbarsFlag="false"
                :editable="false"
            />
        </a-drawer>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>讲座动态</h1>
                            <p class="subheading">抢在第一位～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a-table :columns="columns" :dataSource="lectureList" rowKey="id">
                        <!-- lecturer -->
                        <a slot="lecturer" slot-scope="lecturer, record" @click="previewLecturerInfo(record.lecturerInfo)">{{ lecturer }}</a>
                        <span slot="startDate" slot-scope="startDate">{{ moment(startDate).format('lll') }}</span>
                        <span slot="endDate" slot-scope="endDate">{{ moment(endDate).format('lll') }}</span>
                        <a-tag slot="state" slot-scope="state">{{ state }}</a-tag>
                    </a-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        visible: false,
        lecturerInfo: '',
        columns: [{
            dataIndex: 'title',
            title: '标题'
        }, {
            dataIndex: 'lecturer',
            title: '嘉宾',
            scopedSlots: { customRender: 'lecturer' }
        }, {
            dataIndex: 'address',
            title: '地点'
        }, {
            dataIndex: 'startDate',
            title: '开始时间',
            scopedSlots: { customRender: 'startDate' }
        }, {
            dataIndex: 'endDate',
            title: '结束时间',
            scopedSlots: { customRender: 'endDate' }
        }, {
            dataIndex: 'state',
            title: '状态',
            scopedSlots: { customRender: 'state' }
        }]
    }
  },
  async asyncData({ $axios }) {
    let lectureList = []

    await $axios.get('getLectureList')
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            lectureList = response.data.data
        }
    })

    return {
        lectureList: lectureList
    }
  },
  methods: {
      previewLecturerInfo(val) {
          this.lecturerInfo = val
          this.visible = true
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
</style>
