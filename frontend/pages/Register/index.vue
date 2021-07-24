<template>
    <div class="container">
        <a-row type="flex" justify="center" align="middle">
            <a-col :lg="14" :md="18" :sm="18" :xs="24">
                <a-spin :spinning="spinning">
                    <div class="fh5co-form">
                        <a-row type="flex" class="text-center">
                            <a-col :span="6">
                                <a-button type="primary" @click="$router.push({ path: '/' })">
                                    <a-icon type="left" />返回主页
                                </a-button>
                            </a-col>
                            <a-col :span="6" :offset="12">
                                <a-button type="primary" @click="$router.push({ path: '/login' })">
                                    登录<a-icon type="right" />
                                </a-button>
                            </a-col>
                        </a-row>
                        <hr />
                        <a-form :form="form_register" @submit="register">
                            <a-form-item v-bind="formItemLayout">
                                <span slot="label">
                                    昵称&nbsp;
                                    <a-tooltip title="其他人将会看到您的昵称">
                                        <a-icon type="question-circle-o" />
                                    </a-tooltip>
                                </span>
                                <a-input
                                    v-decorator="[
                                        'username',
                                        {
                                            rules: [{ required: true, message: '请输入昵称', whitespace: true }]
                                        }
                                    ]"
                                >
                                    <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="E-Mail">
                                <a-input
                                    v-decorator="[
                                        'email',
                                        {
                                            rules: [{
                                                type: 'email', message: '请输入有效的EMail',
                                            }, {
                                                required: true, message: '请输入EMail',
                                            }]
                                        }
                                    ]"
                                >
                                    <a-icon slot="prefix" type="mail" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="密码">
                                <a-input
                                    v-decorator="[
                                        'password',
                                        {
                                            rules: [{
                                                required: true, message: '请输入密码',
                                            },
                                            {
                                                validator: validator_password,
                                            }],
                                        }
                                    ]"
                                    type="password"
                                >
                                    <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="确认密码">
                                <a-input
                                    v-decorator="[
                                        'password2',
                                        {
                                            rules: [{
                                                required: true, message: '请输入密码',
                                            }, 
                                            {
                                                validator: validator_password2,
                                            }],
                                        }
                                    ]"
                                    type="password"
                                    @blur="blur_password2"
                                >
                                    <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="性别">
                                <a-select
                                    v-decorator="['gender', {
                                        rules: [{ required: true, message: '请选择您的性别' }],
                                        initialValue: '男'
                                    }]"
                                    placeholder="性别"
                                >
                                    <a-select-option value="男">男</a-select-option>
                                    <a-select-option value="女">女</a-select-option>
                                </a-select>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout">
                                <span slot="label">
                                    个性签名&nbsp;
                                    <a-tooltip title="简略的最自己的描述">
                                        <a-icon type="question-circle-o" />
                                    </a-tooltip>
                                </span>
                                <a-input
                                    v-decorator="[
                                        'bio',
                                        {
                                            rules: [{ required: true, message: '请输入个性签名', whitespace: true }]
                                        }
                                    ]"
                                >
                                    <a-icon slot="prefix" type="edit" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="班级">
                                <a-cascader
                                    v-decorator="[
                                        'class',
                                        {
                                            initialValue: ['zhongyi', 'wuyi'],
                                            rules: [{ type: 'array', required: true, message: '请选择您的班级' }],
                                        }
                                    ]"
                                    :options="classes"
                                />
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="姓" extra="用于实名认证[可选].">
                                <a-input
                                    v-decorator="[
                                        'last_name',
                                    ]"
                                >
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="名" extra="用于实名认证[可选].">
                                <a-input
                                    v-decorator="[
                                        'first_name',
                                    ]"
                                >
                                </a-input>
                            </a-form-item>
                            <!--
                            <a-form-item v-bind="formItemLayout" label="手机" extra="可以和TA更密切的交流[可选].">
                                <a-input
                                    v-decorator="[
                                        'phone',
                                        {
                                            rules: [{
                                                validator: validator_phone
                                            }]
                                        }
                                    ]"
                                    type="number"
                                >
                                    <a-icon slot="prefix" type="phone" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            -->
                            <a-form-item v-bind="formItemLayout" label="QQ" extra="可以和TA更密切的交流[可选].">
                                <a-input
                                    v-decorator="[
                                        'qq'
                                    ]"
                                    type="number"
                                >
                                    <a-icon slot="prefix" type="qq" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="微信" extra="可以和TA更密切的交流[可选].">
                                <a-input
                                    v-decorator="[
                                        'wechat',
                                    ]"
                                >
                                    <a-icon slot="prefix" type="wechat" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="验证码" extra="验证码会发往您的邮箱(邮件可能会在垃圾箱)">
                                <a-row :gutter="8">
                                    <a-col :span="12">
                                        <a-input
                                            v-decorator="['captcha', {
                                                rules: [{ required: true, message: '请输入验证码' }]
                                            }]"
                                        />
                                    </a-col>
                                    <a-col :span="12">
                                        <a-button :disabled="isDisableCaptcha" @click="getCaptcha">{{ CaptchaButtonText }}</a-button>
                                    </a-col>
                                    <a-col :span="12">
                                        <a>微信小程序(正在开发中)</a>
                                    </a-col>
                                </a-row>
                            </a-form-item>
                            <a-form-item v-bind="tailFormItemLayout">
                                <a-checkbox
                                    v-decorator="[
                                        'agreement',
                                        { valuePropName: 'checked' }
                                    ]"
                                >
                                    我同意
                                </a-checkbox>
                                <a @click="showDrawer_agreement=true">用户条款</a>
                                <a-drawer
                                    title="用户条款"
                                    placement="bottom"
                                    :closable="false"
                                    @close="showDrawer_agreement=false"
                                    :visible="showDrawer_agreement"
                                >
                                    <p style="white-space: pre-line">尊敬的客户您好，欢迎您访问寻可校园墙（以下简称： 网站）。在您注册成为网站会员之前， 请您务必认真阅读和理解《网站用户注册协议》 （以下简称：协议）中所有的条款。您须完全同意协议中所有的条款，才可以注册成为本网站的会员，使用里面的服务。您在网站的注册和操作均将被视为是您对协议所有条款及内容的自愿接受。
一、声明
（一）网站内在线产品的所有权归eliotwjz@gmail.com所有。
（二）您在网站进行注册时，一旦点击“注册”按钮，即表示为您已自愿接受协议中所有的条款和内容。
（三）协议条款的效力范围仅限于本网站，您在网站的行为均受协议的约束。
（四）您使用网站服务的行为，即被视为您已知悉本网站的相关公告并同意。
（五）本网站有权在未提前通知您的情况下修改协议的条款，您每次进入网站在使用服务前，都应先查阅一遍协议。
（六）本网站有权在未提前通知您的情况下修改、暂停网站部分或全部的服务，且不承担由此产生来自您和第三方的任何责任。
（七）本网站提供免费注册服务，您的注册均是自愿行为，注册成功后，您可以得到网站更加完善的服务。
（八）您注册成为会员后账户和密码如有灭失，不会影响到您已办理成功业务的效力，本网站可恢复您的注册账户及相关信息但不承担除此以外的其它任何责任。
二、用户管理
（一）您在本网站的所有行为都须符合中国的法律法规，您不得利用本网站提供的服务制作、复制、发布、传播以下信息：
1、反对宪法基本原则的；
2、危害国家安全、 泄露国家秘密、 颠覆国家政权、 破坏国家统一的；
3、损害国家荣誉和利益的；
4、煽动民族仇恨、民族歧视、破坏民族团结的；
5、破坏国家宗教政策，宣扬邪教和封建迷信的；
6、散布谣言、扰乱社会秩序、破坏社会稳定的；
7、散布淫秽、色情、赌博、暴力、凶杀、恐怖内容或者教唆犯罪的；
8、侮辱或者诽谤他人，侵害他人合法权益的；
9、以及法律、法规禁止的其他内容。
（二）您在本网站的行为，还必须符合其它国家和地区的法律规定以及国际法的有关规定。
（三）不得利用本网站从事以下活动：
1、未经允许，进入他人计算机信息网络或者使用他人计算机信息网络的资源；
2、未经允许， 对他人计算机信息网络的功能进行删除、 修改或增加；
3、未经允许， 对他人计算机信息网络中存储、 处理或者传输的数据和应用程序进行删除、修改或者增加；
4、制作、故意传播计算机病毒等破坏性程序的；
5、其他危害计算机信息网络安全的行为。
（四）遵守本网站其他规定和程序：
1、您对自己在本网站中的行为和操作承担全部责任；
2、您承担责任的形式包括但不仅限于， 对受到侵害者进行赔偿、在本网站首先承担了因您的行为导致的行政处罚或侵权损害赔偿责任后，您应给予本网站的等额赔偿；
3、如果本网站发现您传输的信息含有本协议所规定的内容，本网站有权在不通知您的情况下采取包括但不仅限于向国家有关机关报告、保存有关记录、删除该内容及链接地址、关闭服务器、暂停您账号的操作权限、停止向您提供服务等措施。
三、注册会员权利和义务
（一）注册会员有权用本网站提供的服务功能。
（二）注册会员同意遵守包括但不仅限于《中华人民共和国保守国家秘密法》、《中华人民共和国计算机信息系统安全保护条例》 、《计算机软件保护条例》 、《互联网电子公告服务管理规定》 、《互联网信息服务管理办法》等在内的法律、法规。
（三）您注册时有义务提供完整、真实、的个人信息，信息如有变更，应及时更新。
（四）您成为注册会员须妥善保管用户名和密码，用户登录后进行的一切活动均视为是您本人的行为和意愿，您负全部责任。
（五）您在使用本网站服务时，同意且接受本网站提供的各类信息服务。
（六）您使用本网站时，禁止有以下行为：
1、上载、张贴、发送电子邮件或以其他方式传送含有违反国家法律、法规的信息或资料，这些资料包括但不仅限于资讯、资料、文字、软件、音乐、照片、图形、等（下同） ；
2、散布淫秽、色情、赌博、暴力、凶杀、恐怖或者教唆犯罪的资料；
3、冒充任何个人或机构， 或以虚伪不实的方式误导他人以为其与任何人或任何机构有关；
4、通过本网站干扰、 破坏或限制他人计算机软件、 硬件或通讯设备功能的行为；
5、通过本网站跟踪或以其他方式骚扰他人。
四、用户隐私
我们承诺，对您个人的信息和隐私的安全承担保密义务。未经您授权或同意，本网站不会将您的个人资料信息泄露给第三方，但以下情况除外，且本网站不承担任何责任：
（一）政府单位按照中华人民共和国的法律、行政法规、部门规章、司法解释等规范性法律文件（统称“法律法规” ），要求本网站提供的。
（二）由于您将用户和密码告知或泄露给他人，由此导致的个人资料泄露。
（三）包括但不仅限于黑客攻击、计算机病毒侵入或发作、政府管制等不可抗力而造成的用户个人资料泄露、丢失、被盗用或被篡改等。
（四）为免除他人正在遭受威胁到其生命、身体或财产等方面的危险，所采取的措施。
（五）本网站会与其他网站链接，但不对其他网站的隐私政策及内容负责。
（六）此外，您若发现有任何非法使用您的用户账号或安全漏洞的情况，应立即通告本网站。
（七）由于您自身的疏忽、大意等过错所导致的。
（八）您在本网站的有关记录有可能成为您违反法律法规和本协议的证据。
五、知识产权
本网站所有的域名、商号、商标、文字、视像及声音内容、图形及图像均受有关所有权和知识产权法律的保护，未经本网站事先以书面明确允许，任何个人或单位，均不得进行复制和使用。
六、法律适用
（一）协议由本网站的所有人负责修订， 并通过本网站公布，您的注册行为即被视为您自愿接受协议的全部条款，受其约束。
（二）协议的生效、履行、解释及争议的解决均适用中华人民共和国法律。
（三）您使用网站提供的服务如产生争议，原则上双方协商解决，协商不成可向仲裁机构申请仲裁或人民法院提起诉讼。
（四）协议的条款如与法律相抵触， 本网站可进行重新解析，而其他条款则保持对您产生法律效力和约束。
                                    </p>
                                </a-drawer>
                            </a-form-item>
                            <a-form-item v-bind="tailFormItemLayout">
                                <a>已有账号？现在登录～</a>
                                <a-button type="primary" html-type="submit" :disabled="!form_register.getFieldValue('agreement')" style="width: 100%">注册</a-button>
                            </a-form-item>
                        </a-form>
                    </div>
                </a-spin>
            </a-col>
        </a-row>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data () {
    return {
        form_register: this.$form.createForm(this),
        confirmDirty: false,
        showDrawer_agreement: false,
        formItemLayout: {
            labelCol: {
                xs: { span: 24 },
                sm: { span: 6 },
            },
            wrapperCol: {
                xs: { span: 24 },
                sm: { span: 16 },
            },
        },
        tailFormItemLayout: {
            wrapperCol: {
                xs: {
                    span: 24,
                    offset: 0,
                },
                sm: {
                    span: 12,
                    offset: 6,
                },
            },
        },
        isDisableCaptcha: false,
        CaptchaButtonText: '获取',
        spinning: false
    }
  },
  async asyncData({ store, redirect }) {
      if (store.state.userBaseInfo.id != -1) {
          redirect('/')
      }
  },
  methods: {
    blur_password2 (e) {
        let value = e.target.value
        this.confirmDirty = this.confirmDirty || !!value
    },
    validator_password (rule, value, callback) {
      if (value && this.confirmDirty) {
          this.form_register.validateFields(['password2'], { force: true })
      }
      callback()
    },
    validator_password2 (rule, value, callback) {
        if (value && value !== this.form_register.getFieldValue('password')) {
            callback('两次密码不一致')
        } else {
            callback()
        }
    },
    /*
    validator_phone (rule, value, callback) {
        var regex_phone = /^1[345789]\d{9}$/
        if (value && !regex_phone.test(value)) {
            callback('请输入合法的手机号')
        }
        callback()
    },
    */
    register(e) {
        this.spinning = true
        e.preventDefault()
        this.form_register.validateFields((err, values) => {
            if (!err) {
                this.$axios.post('register', qs.stringify({
                    email: values.email,
                    username: values.username,
                    password: values.password,
                    bio: values.bio,
                    gender: values.gender,
                    class: values.class,
                    last_name: values.last_name,
                    first_name: values.first_name,
                    //phone: values.phone,
                    qq: values.qq,
                    wechat: values.wechat,
                    captcha: values.captcha
                }))
                .then((response) => {
                    this.spinning = false
                    if (response.data.code == 200 && response.data.status == 'success') {
                        this.$message.success('注册成功')
                        this.$router.push({ path: '/login' })
                    }
                })
            }
        })
    },
    getCaptcha() {
        var email = this.form_register.getFieldValue('email')
        if (email) {
            this.$axios.get('getCaptcha', {
                params: {
                    email: email
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.$message.success('验证码已发往您的邮箱，有效期为3分钟，请查收')
                }
            })

            this.isDisableCaptcha = true
            let time = 60
            var countDown = setInterval(() => {
                time --
                if (time == 0) {
                    this.isDisableCaptcha = false
                    this.CaptchaButtonText = '获取'
                    clearInterval(countDown)
                }
                else {
                    this.CaptchaButtonText = time.toString() + '后重新获取'
                }
            }, 1000)
        }
        else {
            this.$message.error('请输入您的邮箱')
        }
    }
  },
  computed: mapState({
    classes: state => state.classes,
  })
}
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
