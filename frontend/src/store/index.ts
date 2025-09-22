import { createStore } from 'vuex'

export interface RootState {
  health: { reachable: boolean | null }
  rateLimited: boolean
}

const store = createStore<RootState>({
  state: {
    health: { reachable: null },
    rateLimited: false,
  },
  mutations: {
    setHealth(state, reachable: boolean | null) {
      state.health.reachable = reachable
    },
    setRateLimited(state, value: boolean) {
      state.rateLimited = value
    },
  },
  actions: {},
  modules: {},
})

export default store
