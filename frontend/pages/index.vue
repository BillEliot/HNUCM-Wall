<template>
  <div>
    <header>
      <!-- navbar -->
      <a-menu v-model="navbar" mode="horizontal" theme="dark" class="nav">
        <a-sub-menu>
          <span slot="title"><a-icon type="coffee" />表白墙</span>
          <a-menu-item-group title="I Love U">
            <a-menu-item key="love:1">表白墙</a-menu-item>
            <a-menu-item key="love:2">我要表白</a-menu-item>
          </a-menu-item-group>
        </a-sub-menu>

        <a-menu-item key="whisper">
          <a-icon type="star" /> 悄悄话
        </a-menu-item>
        <!-- login/register -->
        <template v-if="username">
          <a-avatar :src="avatar" />
          <a-dropdown>
            <a> {{ username }} <a-icon type="down" /></a>
            <a-menu slot="overlay">
              <a-menu-item>
                <router-link to="/profile">个人信息</router-link>
              </a-menu-item>
              <a-menu-item @click="logout">注销</a-menu-item>
              <a-menu-item>
                <router-link to="/reserve">立即预约</router-link>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </template>
        <template v-else>
          <router-link to="/login">
            <a-button type="primary" style="margin-right: 10px">登录</a-button>
          </router-link>
          <router-link to="/register">
            <a-button>注册</a-button>
          </router-link>
        </template>
      </a-menu>

      <a-carousel autoplay>
        <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
        <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1558497293209&di=48b70276e02fd17a558683fd8c62b0e4&imgtype=0&src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fblog%2F201503%2F07%2F20150307163030_aRPTy.jpeg">
      </a-carousel>
      <!--
      <div class="hero-holder" style="position: relative">
        <div class="hero-message">
          <h1 class="uppercase">优敏思</h1>
          <h2 class="hero-subtitle">竞赛教育领跑者</h2>
        </div>
      </div>
      -->
    </header>

    <div style="margin-top: 100px"></div>

    <div class="container">
      <div class="row">
        <!-- Top -->
        <a-card hoverable style="width: 100%">
          <template class="ant-card-actions" slot="actions">
            <a-icon type="setting" />
            <a-icon type="edit" />
            <a-icon type="ellipsis" />
          </template>
          <a-card-meta
            title="Card title"
            description="This is the description">
            <a-avatar slot="avatar" src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
          </a-card-meta>
          <img
            src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
            slot="cover"
            style="height: 200px"
          />
        </a-card>
        <!-- List -->
        <div v-infinite-scroll="handleInfiniteOnLoad" :infinite-scroll-disabled="busy" :infinite-scroll-distance="10">
          <a-list :dataSource="listData" itemLayout="vertical" size="large">
            <div slot="footer"><b>ant design vue</b> footer part</div>
            <a-list-item slot="renderItem" slot-scope="item, index" key="item.title">
              <template slot="actions" v-for="{type, text} in actions">
                <span :key="type">
                  <a-icon :type="type" style="margin-right: 8px" />
                  {{text}}
                </span>
              </template>
              <img slot="extra" width="272" alt="logo" src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png" />
              <a-list-item-meta :description="item.description">
                <a slot="title" :href="item.href">{{item.title}}</a>
                <a-avatar slot="avatar" :src="item.avatar" />
              </a-list-item-meta>
              {{item.content}}
            </a-list-item>
          </a-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const listData = []
for (let i = 0; i < 5; i++) {
  listData.push({
    href: 'https://vue.ant.design/',
    title: `ant design vue part ${i}`,
    avatar: 'https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png',
    description: 'Ant Design, a design language for background applications, is refined by Ant UED Team.',
    content: 'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
  })
}

export default {
  name: 'Home',
  data() {
    return {
      navbar: null,
      username: null,

      listData,
      actions: [
        { type: 'like-o', text: '156' },
        { type: 'message', text: '2' },
      ],
    }
  }
}
</script>

<style>

</style>
