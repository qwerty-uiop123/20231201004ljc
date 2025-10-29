import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { TiebaInfo, PostInfo, TiebaCategory, SearchTiebaParams } from '@/types/tieba'
import { tiebaApi, postApi } from '@/services/tieba'
import { useGlobalStore } from '@/stores/global'

export const useTiebaStore = defineStore('tieba', () => {
  const globalStore = useGlobalStore()
  
  // 当前贴吧信息
  const currentTieba = ref<TiebaInfo | null>(null)
  
  // 贴吧列表
  const tiebaList = ref<TiebaInfo[]>([])
  
  // 帖子列表
  const postList = ref<PostInfo[]>([])
  
  // 分类列表
  const categories = ref<TiebaCategory[]>([])
  
  // 热门贴吧
  const hotTiebas = ref<TiebaInfo[]>([])
  
  // 推荐贴吧
  const recommendedTiebas = ref<TiebaInfo[]>([])
  
  // 搜索历史
  const searchHistory = ref<string[]>([])
  
  // 加载状态
  const loading = ref(false)
  
  // 获取贴吧详情
  const getTiebaDetail = async (tiebaId: number) => {
    loading.value = true
    try {
      const response = await tiebaApi.getTiebaDetail(tiebaId)
      currentTieba.value = response
      return { success: true, data: response }
    } catch (error: any) {
      const message = error.response?.data?.detail || '获取贴吧详情失败'
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }
  
  // 获取贴吧帖子列表
  // 获取帖子列表
  const getPostList = async (tiebaId: number, page = 1, pageSize = 20) => {
    loading.value = true
    try {
      const response = await postApi.getPosts({
        tieba: tiebaId,
        page,
        page_size: pageSize
      })
      
      if (page === 1) {
        postList.value = response.results || response
      } else {
        postList.value.push(...(response.results || response))
      }
      
      const hasMore = response.next !== null
      return { success: true, data: response.results || response, hasMore }
    } catch (error: any) {
      const message = error.response?.data?.detail || '获取帖子列表失败'
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }
  
  // 搜索贴吧
  const searchTiebas = async (params: SearchTiebaParams) => {
    loading.value = true
    try {
      const response = await tiebaApi.getTiebas({
        search: params.keyword,
        category: params.category,
        page: params.page,
        page_size: params.pageSize
      })
      
      tiebaList.value = response.results || response
      
      // 添加到搜索历史
      if (params.keyword && !searchHistory.value.includes(params.keyword)) {
        searchHistory.value.unshift(params.keyword)
        if (searchHistory.value.length > 10) {
          searchHistory.value.pop()
        }
      }
      
      return { success: true, data: response.results || response }
    } catch (error: any) {
      const message = error.response?.data?.detail || '搜索贴吧失败'
      return { success: false, message }
    } finally {
      loading.value = false
    }
  }
  
  // 加入贴吧
  const joinTieba = async (tiebaId: number) => {
    try {
      await tiebaApi.joinTieba(tiebaId)
      
      // 更新当前贴吧的加入状态
      if (currentTieba.value && currentTieba.value.id === tiebaId) {
        currentTieba.value.isJoined = true
        currentTieba.value.memberCount += 1
      }
      
      globalStore.showMessage('加入贴吧成功', 'success')
      return { success: true }
    } catch (error: any) {
      const message = error.response?.data?.detail || '加入贴吧失败'
      globalStore.showMessage(message, 'error')
      return { success: false, message }
    }
  }
  
  // 退出贴吧
  const leaveTieba = async (tiebaId: number) => {
    try {
      await tiebaApi.leaveTieba(tiebaId)
      
      // 更新当前贴吧的加入状态
      if (currentTieba.value && currentTieba.value.id === tiebaId) {
        currentTieba.value.isJoined = false
        currentTieba.value.memberCount -= 1
      }
      
      globalStore.showMessage('退出贴吧成功', 'success')
      return { success: true }
    } catch (error: any) {
      const message = error.response?.data?.detail || '退出贴吧失败'
      globalStore.showMessage(message, 'error')
      return { success: false, message }
    }
  }
  
  // 获取热门贴吧
  const getHotTiebas = async () => {
    try {
      const response = await tiebaApi.getTiebas({
        sort: '-member_count',
        page_size: 10
      })
      
      hotTiebas.value = response.results || response
      return { success: true, data: response.results || response }
    } catch (error: any) {
      const message = error.response?.data?.detail || '获取热门贴吧失败'
      return { success: false, message }
    }
  }
  
  // 获取推荐贴吧
  const getRecommendedTiebas = async () => {
    try {
      const response = await tiebaApi.getTiebas({
        sort: '-post_count',
        page_size: 10
      })
      
      recommendedTiebas.value = response.results || response
      return { success: true, data: response.results || response }
    } catch (error: any) {
      const message = error.response?.data?.detail || '获取推荐贴吧失败'
      return { success: false, message }
    }
  }
  
  // 清空搜索历史
  const clearSearchHistory = () => {
    searchHistory.value = []
  }
  
  return {
    currentTieba,
    tiebaList,
    postList,
    categories,
    hotTiebas,
    recommendedTiebas,
    searchHistory,
    loading,
    getTiebaDetail,
    getPostList,
    searchTiebas,
    joinTieba,
    leaveTieba,
    getHotTiebas,
    getRecommendedTiebas,
    clearSearchHistory
  }
})