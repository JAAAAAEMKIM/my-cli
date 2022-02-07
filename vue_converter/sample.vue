<template>
  <div class="preview-image-modal"
       :style="`z-index: ${modalZIndex}`"
       v-if="dialog"
       tabindex="0"
       @keydown="onKeydown"
       @click="onClose"
  >

  <template></template>
    <div class="preview-image-modal-body" :style="{width: `${width}px`, height: `${height}px`}" @click.stop>
      <div class="preview-image-modal-header">
        <div class="modal-button-group">
          <button-a size="s" @click="onPrevImg">
            <i class="icon-left-12" />
            <translate>home.post_detail~~이전</translate>
          </button-a>
          <button-a size="s" @click="onNextImg">
            <translate>home.post_detail~~다음</translate>
            <i class="icon-right-12" />``
          </button-a>
        </div>
        <i class="v2-icons-attach-x" @click="onClose" />
      </div>
      <div class="preview-image-modal-content" :style="{height: `${height - 67}px`}">
        <h2>{{ currentFile.name }}</h2>
        <img :style="{width: horizontal ? '100%' : '', height: horizontal ? '' : '100%'}"
             :src="currentFile.downloadUrl"
             :alt="currentFile.name"
             ref="img"
             :title="'home.post_detail~~원본 보기' | translate"
             @load="onLoadImg"
             @click="onNewTab(currentFile)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Model, Prop, Vue, Watch} from 'vue-property-decorator';

import {FormDialog, SelectDropdown, SelectDropdownItem} from '@dooray-ui-kit';

interface Category {
  id: string;
  name: string;
}

@Component({
  components: {
    FormDialog,
    SelectDropdown,
    SelectDropdownItem
  }
})
export default class CategoryChangeDialog extends Vue {
  @Model('change', {type: Boolean, default: false}) dialog: boolean;
  @Prop({type: Array, default: () => []}) categories: Category[];
  @Prop({type: String, default: ''}) removeCategoryId: string;

  changeCategoryId = '';

  get items() {
    return this.categories.filter(category => category.id !== this.removeCategoryId)
      .map(category => ({
        value: category.id,
        label: category.name
      }));
  }

  @Watch('removeCategoryId')
  watchRemoveCategoryId() {
    const items = this.items;
    this.changeCategoryId = items.length ? items[0].value : '';
  }

  onChange(value: boolean) {
    this.$emit('change', value);
  }

  onClose(value: string) {
    this.$emit('close', value, this.changeCategoryId);
  }
}
</script>

<style lang="scss" scoped>
.category-change-dialog {

  .title {
    font-size: 16px;
    font-weight: 700;
    font-style: normal;
    color: #222;
  }

  .change-form {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-top: 12px;
  }

  .margin-left-5 {
    margin-left: 5px;
  }
}
</style>
