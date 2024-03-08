<template>
    <el-container>

        <el-header>
            <h1>牛皮糖翻译</h1>
        </el-header>

        <el-main style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <el-row class="row-bg" justify="center">
                <el-col>
                    <el-input class="textarea" type="textarea" :autosize="{ minRows: 10, maxRows: 30 }" v-model="msg"
                        placeholder="请输入要翻译的内容..."></el-input>
                </el-col>
                <el-col>
                    <span>目标语言: </span>
                    <el-select v-model="targetLang" placeholder="Select" size="large" style="width: 240px">
                        <el-option v-for="item in langs" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </el-col>
                <el-col>
                    <el-button color="#626aef" :dark="isDark" style="width: 100px;" :loading="translateButtonLoading"
                        v-on:click="translate()">
                        <template #loading>
                            <div class="custom-loading">
                                <svg class="circular" viewBox="-10, -10, 50, 50">
                                <path
                                    class="path"
                                    d="
                                    M 30 15
                                    L 28 17
                                    M 25.61 25.61
                                    A 15 15, 0, 0, 1, 15 30
                                    A 15 15, 0, 1, 1, 27.99 7.5
                                    L 15 15
                                "
                                    style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"
                                />
                                </svg>
                            </div>
                            </template>
                            {{ translateButtonLoading ? '翻译中...' : '翻译' }}
                        </el-button>
                </el-col>
            </el-row>
            <el-divider />
            <el-row class="row-bg translate-result" justify="center">
                {{ translateResult }}
            </el-row>
        </el-main>

    </el-container>
</template>

<script>

import { ElButton, ElInput } from 'element-plus';
import api from '@/api/translate';
export default {
    name: 'IndexPage',
    components: {
        ElButton, ElInput
    },
    data() {
        return {
            msg: '',
            langs: [
                {
                    value: 'ZH',
                    label: '中文'
                },
                {
                    value: 'EN',
                    label: 'English'
                }
            ],
            targetLang: 'ZH',
            isDark: false,
            translateButtonLoading: false,
            translateResult: ""
        }
    },
    methods: {
        translate() {
            this.translateButtonLoading = true
            console.log(this.msg);
            const data = {
                text: this.msg,
                target_lang: this.targetLang
            }
            api.translate(data, th => th.then((res) => {
                console.log(res.data);
                let response = res.data
                this.translateResult = response.data;
            }).finally(() => {
                this.translateButtonLoading = false
            }))
        }
    }
}
</script>

<style>
.el-col {
    border-radius: 4px;
    margin-bottom: 20px;
}

.textarea {
    max-width: 700px;
    min-width: 330px;
}


.el-button .custom-loading .circular {
  margin-right: 6px;
  width: 18px;
  height: 18px;
  animation: loading-rotate 2s linear infinite;
}
.el-button .custom-loading .circular .path {
  animation: loading-dash 1.5s ease-in-out infinite;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-width: 2;
  stroke: var(--el-button-text-color);
  stroke-linecap: round;
}

.translate-result {
    text-align: start;
    max-width: 700px;
    white-space: pre-line;
}
</style>