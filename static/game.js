let currGame;

$('#start-game').on('click', function () {
    currGame = new Game();
    $('#start-game')[0].style.display = 'none'
    $('#form')[0].style.display = 'flex'
})


$('#form').on('submit', async function (e) {
    e.preventDefault();
    const guess = e.target.elements[0].value;
    await currGame.check_guess(guess)
    $('#guess')[0].value = ''
});

$('#new-btn').on('click', function () {
    location.reload()
})

let time = 60;
class Game{
    constructor(){
        this.score =0;
        this.countdown = setInterval(function () {
            
            if (time > 0) {
                time--;
                $('#time')[0].innerText = time
            }
            if (time === 0) {
                currGame.endgame()
            }
        }, 1000);
    }

    async check_guess(guess) {
        const checked = await axios.get(`/guess?guess=${guess}`)
        const isFound = checked.data['found']
        const isChecked = checked.data['on_board']
        this.displayMessage(isChecked, isFound)
        if (isFound === false && isChecked === "ok") {
            this.score++;
            console.log("Found new word")
            await axios({
                url: 'http://127.0.0.1:5000/found',
                method: 'POST',
                data: { 'guess': guess }
            })
            $('#score')[0].innerText = this.score
        }
    }

    displayMessage(status, found) {
        if (found) {
            $('#message')[0].innerText = 'Already Found Word'
            return;
        }
        switch (status) {
            case 'ok':
                $('#message')[0].innerText = 'Found New Word'
                break;
            case 'not-on-board':
                $('#message')[0].innerText = "Word Not On Board"
                break;
            case 'not-word':
                $('#message')[0].innerText = 'Not A Word'
                break;
        }
    }

    async endgame() {
        clearInterval(this.countdown)
        console.log('GAME OVER!')
        $('#form-btn')[0].disabled = true;
        $('#endgame')[0].style.display = 'flex'
        const getHigh = await axios.get(`/end-game? score=${this.score}`)
        const highScore = getHigh.data.high_score
        $('#end-score')[0].innerText = this.score
        $('#end-high')[0].innerText = highScore
        if (this.score === highScore) {
            $('#new-high')[0].style.display = 'flex'
        }
    }
}