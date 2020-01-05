export const state = () => ({
    timer: null,
    questions: [],
    subjects: [],
    currentSubject: ''
})

export const getters = {
    getChapters: (state) => (value) => {
        return state.subjects.filter((chapter) => {
            return chapter.key == value
        })[0].chapters
    }
}

export const mutations = {
    setSubjects(state, subjects) {
        state.subjects = subjects
    },
    setQuestions(state, questions) {
        state.questions = questions
    },
    setCurrentSubject(state, currentSubject) {
        state.currentSubject = currentSubject
    },
    setTimer(state, timer) {
        state.timer = timer
    }
}

export const actions = {
    setBank({ commit }, { questions, timer, subject }) {
        commit('setQuestions', questions)
        commit('setTimer', timer),
        commit('setCurrentSubject', subject)
    },
}
