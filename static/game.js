
$('#form').on('submit', async function (e) {
    e.preventDefault();
    const guess = e.target.elements[0].value;
    const valid = await check_guess(guess)
    console.log(valid)
});

async function check_guess(guess) {
    const checked = await axios.get(`/guess?guess=${guess}`)
    return checked
}