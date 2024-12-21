<template>
    <div class="container">
        <!-- Left Column -->
        <div class="left-column">
            <div class="image-wrapper">
                <img class="image-back" src="@/assets/introBig.jpg" alt="Background image" />
                <img class="image-front" src="@/assets/introSmall.jpg" alt="Foreground image" />
            </div>
        </div>

        <!-- Right Column -->
        <div class="right-column">
            <h1 class="title"> Our Attitude Towards Customers</h1>
            <div class="services">
                <div class="service-column">
                    <div class="service">
                        <h2 class="small-title">Respect</h2>
                        <p>We treat every customer with the utmost respect, ensuring their voices are heard and their
                            concerns are valued.</p>
                    </div>
                    <div class="service">
                        <h2 class="small-title">Responsiveness</h2>
                        <p>Our team is dedicated to addressing customer needs promptly and providing clear, timely
                            communication.</p>
                    </div>
                </div>
                <div class="service-column">
                    <div class="service">
                        <h2 class="small-title">Empathy</h2>
                        <p>We strive to understand our customers' perspectives and offer solutions that align with their
                            unique situations.</p>
                    </div>
                    <div class="service">
                        <h2 class="small-title">Commitment</h2>
                        <p>Our unwavering commitment to excellence ensures we go above and beyond to deliver exceptional
                            service.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CustomerAttitude",
};
</script>

<style scoped>
.container {
    display: flex;
    gap: 2rem;
    padding: 2rem;
    margin-bottom: 60px;
    margin-top: 50px;
}

.left-column {
    flex: 1;
    position: relative;
}

.image-wrapper {
    position: relative;
    height: 300px;
}

.image-back {
    position: absolute;
    top: -15%;
    width: 65%;
    border-radius: 50% / 25%;
}

.image-front {
    position: absolute;
    top: 25%;
    left: 38%;
    width: 50%;
    border-radius: 50% / 25%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    height: 390px;
}

.right-column {
    flex: 1;
    text-align: left;
    /* Align text to the left */
}

h1 {
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: left;
    /* Align title to the left */
}

.services {
    display: flex;
    gap: 2rem;
}

.service-column {
    flex: 1;
}

.service {
    margin-bottom: 1.5rem;
}

h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    text-align: left;
    /* Align headings to the left */
}

p {
    font-size: 1rem;
    line-height: 1.5;
    text-align: left;
    /* Align paragraphs to the left */
}

.title {
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}

.small-title {
    font-weight: 550;
}
</style>
