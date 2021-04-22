<template>
    <div >
        <div class="info-card row no-wrap">
            <div class="penals col-4">
                <head-card />
                <q-tabs
                v-model="tab"
                vertical
                class="text-teal"
                >
                    <q-tab name="infomation" icon="infomation" label="Personal Information" />
                    <q-tab name="history" icon="history" label="Balance">
                        <q-badge color="orange" floating>{{historyNum}}</q-badge>
                    </q-tab>
                    <q-tab name="bookmark" icon="bookmark" label="Records of Comsumptions">
                        <q-badge color="orange" floating>{{favoriteNum}}</q-badge>
                    </q-tab>
                </q-tabs>
            </div>

            <q-separator vertical />
    
            <div class="info-display col-8">
                <q-tab-panels
                v-model="tab"
                animated
                vertical
                transition-prev="jump-up"
                transition-next="jump-up"
                >
                <q-tab-panel name="infomation">
                    <div class="text-h4 q-mb-md">Modify Personal Information</div>
                    <user-info  class="edit-form"/>
                </q-tab-panel>

                <q-tab-panel name="history">
                    <div class="text-h4 q-mb-md">Balance</div>
                    <div class="text-h1">HK${{ userInfo.balance }}</div>
                    <!--<q-label name="balance" class="balance text-overline"> {{ userInfo.balance }} </q-label>-->
                    <div class=" q-gutter-md input-form">
                        <q-input v-model="balance" label="Consumption Amount"/>
                        <q-btn class="full-width" color="primary" :loading="isLoading" :disable="b_IsValide" @click="handleConsumptionClick">
                            CONFIRM
                        </q-btn>
                    </div>
                </q-tab-panel>

                <q-tab-panel name="bookmark">
                    <div class="text-h4 q-mb-md">Records of Comsumptions</div>
                    <!-- 收藏的消息 -->

                    <history-news v-for="news in newsList" :key="news.id" :news="news"/>
                    <div v-if="newsList.length==0" class="text-h5">None</div>
                </q-tab-panel>
                </q-tab-panels>
            </div>
        </div>
    </div>
</template>

<script>
import headCard from './headCard'
import historyNews from './historyNews'
import userInfo from './userInfo'

import {mapState} from 'vuex'

export default {
    components:{
        headCard,
        historyNews,
        userInfo
    },
    data(){
        return {
            tab: 'infomation',
            splitterModel: 50,
            balance: ''
        }
    },
    computed:{
        historyNum(){
            return 10;//this.balance
        },
        favoriteNum(){
            return this.newsList.length ;
        },
        ...mapState('favorite', ['newsList', 'isLoading']),
        ...mapState('userInfo', ['isLoading', 'userInfo']),
        b_IsValide(){
            if(
                this.balance > this.userInfo.balance 
            ){
                return true
            }
            return false
        }, 
    },
    methods:{
        handleConsumptionClick(){
            console.log(this.userInfo.balance-this.balance)
            this.$store.dispatch('userInfo/setBalance', this.userInfo.balance-this.balance)
            console.log(this.userInfo.balance)
        }
    },
    props:{
        nickname:{
            default:"nickname"
        },
        account:{
            default:"account"
        }
    }
}
</script>

<style scoped>

.info-card{
    width:100%;
    padding:10px
}
.edit-form{
    padding:10px;
    margin-left:20px
}
.penals{
    width:300px;
    height:800px;
}

.info-display{
    margin-left:40px;
    height:800px;
    /* border:1px black solid */
}

.input-form{
    max-width:300px
}
</style>