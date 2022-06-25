<template>

    <div class="card">
        <h2 class="card__header">
            <slot name="header">
                
            </slot>
        </h2>

        <slot></slot>
    </div>
</template>

<style scoped lang="scss">

.card{
    background-color: $color-white;
    width: 100%;
    min-height: 50px;
    padding: 25px 35px;
    box-shadow: 0px 8px 16px rgba(17, 17, 17, 0.06);
    border-radius: 12px;
    box-sizing: border-box;
    &__header{
        margin-top:0;
        margin-bottom: 10px;
        font-style: normal;
        font-weight: 400;
        font-size: 24px;
        line-height: 38px;
        letter-spacing: 0.75px;
        color: $color-text-main;
    }
}

</style>