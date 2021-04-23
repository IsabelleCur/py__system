<template>
    <q-card  class=" fixed-center reg-form bg-grey text-white">
        <q-card-section class="head">
            <div class="head-title text-h4">E-Voucher</div>
            <div class="head-subtitle text-subtitle2">Registration</div>
        </q-card-section>



        <q-card-section class="reg-form-input">
            <q-input outlined v-model="account" label="ID card number" :rules="[val => !!val || 'Please enter your ID card number']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="nickname" label="nickname" :rules="[val => !!val || 'Please enter your nickname']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="name" label="name" :rules="[val => !!val || 'Please enter your name']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="number" label="number" :rules="[val => !!val || 'Please enter your number']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="gender" label="gender(M/F)" :rules="[val => !!val || 'Please enter your gender']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="birth" label="birth(XX-XX-XXXX)" :rules="[val => !!val || 'Please enter your date of birth']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="person" />
                </template>
            </q-input>
            <q-input outlined v-model="password" type="password" label="password" :rules="[val => !!val || 'Please enter your password']" @input="isValidate">
                <template v-slot:prepend>
                    <q-icon name="apps" />
                </template>
            </q-input>
        </q-card-section>

        <q-card-actions class="reg-form-bottom">
            <q-toggle class="accept-term" v-model="accept" label="I accept the license and terms" @input="isValidate"/>
            <q-btn :disable="disable" border color="primary" class="full-width" @click="handleReg()" >Sign Up</q-btn>
        </q-card-actions>

        <!-- 加载 -->
        <q-inner-loading :showing="isLoading">
            <q-spinner size="50px" color="primary" />
        </q-inner-loading>

    </q-card>
</template>

<script>
import {mapState} from 'vuex'

export default {
    data(){
        return{
            account:'',
            nickname:'',
            name:'',
            number:'',
            gender:'',
            birth:'',
            password:'',
            accept:false,
            disable:true,
        }
    },
    methods:{
        isValidate(){
            if(this.nickname.length > 0 && this.account.length > 0 && this.password.length > 0 && this.accept){
                this.disable = false;
            }
            else this.disable = true;
        },
        async handleReg(){
            var payload = {
                account : this.account,
                nickname : this.nickname,
                name:this.name,
                number:this.number,
                gender:this.gender,
                birth:this.birth,
                password : this.password,
            }
            this.$store.dispatch("userInfo/regUser",payload).then(() =>{
                if(this.userInfo && this.isLoading){
                    if(this.userInfo && this.isLoading){
                        setTimeout(() => {
                            this.$router.push({
                                name:"homepage",
                                params:{
                                    account:this.userInfo.account,
                                }
                            })
                        }, 1000)
                    }
                }
            })
            console.log(this.nickname)
            
        },
    },

    computed: mapState("userInfo", ["isLoading", "userInfo"]),
}
</script>

<style scoped>
.head {text-align: center;padding:30px}
.head-subtitle{padding-top:0px}

.reg-form{width:520px; height: 700px}
.reg-form .reg-form-input{width:300px; margin: 0 auto; position: relative; top:-35px}

.reg-form .reg-form-bottom {width:300px; margin: 0 auto; position: relative; top:-75px}

.reg-form .reg-form-bottom .accept-term{margin:0 auto; padding-bottom: 0px;}

</style>