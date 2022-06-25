<template>
    <div class="select-input">



        <div class="select-menu">
        </div>
    </div>
    
</template>

<style scoped lang="scss">

.select-input{
    height: 56px;
    width: 100%;
    @include input-like;
}

.select-menu{
    width: 100%;
    @include input-like;
    position: absolute;
}

</style>

