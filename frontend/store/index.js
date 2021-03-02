export const state = () => ({
  baseUrl: process.env.NODE_ENV == 'production' ? 'https://hnucmwall.top' : 'http://localhost:8000',
  userBaseInfo: {
    id: -1,
    username: '赶快登陆吧～',
    avatar: '/media/img/avatar/anony.jpg',
    isAdmin: false
  },
  classes: [{
    value: '中医学院',
    label: '中医学院',
    children: [{
      value: '五年制一班',
      label: '五年制一班',
    }, {
      value: '五年制二班',
      label: '五年制二班',
    }, {
      value: '五年制三班',
      label: '五年制三班',
    }, {
      value: '五年制四班',
      label: '五年制四班',
    }, {
      value: '五年制五班',
      label: '五年制五班',
    }, {
      value: '五年制六班',
      label: '五年制六班',
    }, {
      value: '五年制七班',
      label: '五年制七班',
    }, {
      value: '五年制十班',
      label: '五年制十班',
    }, {
      value: '八年制拔尖班',
      label: '八年制拔尖班',
    }, {
      value: '八年制一班',
      label: '八年制一班',
    }, {
      value: '八年制二班',
      label: '八年制二班',
    }, {
      value: '八年制三班',
      label: '八年制三班',
    }],
  }, {
    value: '针灸推拿学院',
    label: '针灸推拿学院',
    children: [{
      value: '针灸推拿一班',
      label: '针灸推拿一班',
    }, {
      value: '针灸推拿二班',
      label: '针灸推拿二班',
    }, {
      value: '针灸推拿三班',
      label: '针灸推拿三班',
    }, {
      value: '针灸推拿四班',
      label: '针灸推拿四班',
    }, {
      value: '针灸推拿五班',
      label: '针灸推拿五班',
    }, {
      value: '针灸推拿六班',
      label: '针灸推拿六班',
    }, {
      value: '康复治疗一班',
      label: '康复治疗一班',
    }, {
      value: '康复治疗二班',
      label: '康复治疗二班',
    }, {
      value: '运动康复班',
      label: '运动康复班',
    }]
  }, {
    value: '中西医结合学院',
    label: '中西医结合学院',
    children: [{
      value: '中西医临床医学一班',
      label: '中西医临床医学一班',
    }, {
      value: '中西医临床医学二班',
      label: '中西医临床医学二班',
    }, {
      value: '中西医临床医学三班',
      label: '中西医临床医学三班',
    }, {
      value: '中西医临床医学四班',
      label: '中西医临床医学四班',
    }, {
      value: '中西医临床医学五班',
      label: '中西医临床医学五班',
    }]
  }, {
    value: '人文与管理学院',
    label: '人文与管理学院',
    children: [{
      value: '英语一班',
      label: '英语一班',
    }, {
      value: '英语二班',
      label: '英语二班',
    }, {
      value: '市场营销一班',
      label: '市场营销一班',
    }, {
      value: '市场营销二班',
      label: '市场营销二班',
    }, {
      value: '应用心理学一班',
      label: '应用心理学一班',
    }, {
      value: '应用心理学二班',
      label: '应用心理学二班',
    }, {
      value: '公共事业管理班',
      label: '公共事业管理班',
    }]
  }, {
    value: '马克思主义学院',
    label: '马克思主义学院',
    children: [{
      value: '马克思主义学院',
      label: '马克思主义学院',
    }]
  }, {
    value: '信息科学与工程学院',
    label: '信息科学与工程学院',
    children: [{
      value: '计算机科学与技术一班',
      label: '计算机科学与技术一班',
    }, {
      value: '计算机科学与技术二班',
      label: '计算机科学与技术二班',
    }, {
      value: '信息管理与信息系统班',
      label: '信息管理与信息系统班',
    }, {
      value: '医学信息工程班',
      label: '医学信息工程班',
    }]
  }, {
    value: '护理学院',
    label: '护理学院',
    children: [{
      value: '护理学一班',
      label: '护理学一班',
    }, {
      value: '护理学二班',
      label: '护理学二班',
    }, {
      value: '护理学三班',
      label: '护理学三班',
    }, {
      value: '护理学四班',
      label: '护理学四班',
    }, {
      value: '护理学五班',
      label: '护理学五班',
    }, {
      value: '护理学六班',
      label: '护理学六班',
    }]
  }, {
    value: '医学院',
    label: '医学院',
    children: [{
      value: '医学院',
      label: '医学院',
    }]
  }, {
    value: '药学院',
    label: '药学院',
    children: [{
      value: '药学院',
      label: '药学院',
    }]
  }, {
    value: '湘杏学院',
    label: '湘杏学院',
    children: [{
      value: '湘杏学院',
      label: '湘杏学院',
    }]
  }, {
    value: '研究生院',
    label: '研究生院',
    children: [{
      value: '研究生院',
      label: '研究生院',
    }]
  }, {
    value: '国际教育学院',
    label: '国际教育学院',
    children: [{
      value: '国际教育学院',
      label: '国际教育学院',
    }]
  }, {
    value: '继续教育学院',
    label: '继续教育学院',
    children: [{
      value: '继续教育学院',
      label: '继续教育学院',
    }]
  }, {
    value: '体育艺术学院',
    label: '体育艺术学院',
    children: [{
      value: '体育艺术学院',
      label: '体育艺术学院',
    }]
  }, {
    value: '第一中医临床学院',
    label: '第一中医临床学院',
    children: [{
      value: '第一中医临床学院',
      label: '第一中医临床学院',
    }]
  }, {
    value: '第二中医临床学院',
    label: '第二中医临床学院',
    children: [{
      value: '第二中医临床学院',
      label: '第二中医临床学院',
    }]
  }, {
    value: '临床医学院',
    label: '临床医学院',
    children: [{
      value: '临床医学院',
      label: '临床医学院',
    }]
  }]
})

export const mutations = {
  setUserBaseInfo(state, userBaseInfo) {
    state.userBaseInfo = userBaseInfo
  },
  clearUserBaseInfo(state) {
    state.userBaseInfo.id = -1
    state.userBaseInfo.username = '赶快登录吧～'
    state.userBaseInfo.avatar = '/media/img/avatar/anony.jpg'
  }
}
