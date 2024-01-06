(function( $ ) {

    class MasterMindApi {
        constructor(settings) {
            this.board = settings.board;
            this.colors = settings.colors;
            this.gameHandlerUrl = settings.gameHandlerUrl;
            this.guessHandlerUrl = null;
        }

        init() {
            let self = this;

            this.board.find('.guess').on('click', '.answer-cell', function () {
                let color = $(this).data('color') ? $(this).data('color') : null;
                let index = color !== null ? self.colors.indexOf(color) : -1;
                if (index === self.colors.length - 1) {
                    index = -1;
                }
                color = self.colors[index + 1];
                $(this).data('color', color);
                $(this).css('background', color);
            });

            this.board.on('click', '#start', function () {
                self.clearBoard();
                self.pollGame(
                    function (res, status, jqXHR) {
                        self.guessHandlerUrl = res.guessHandlerUrl;
                        self.board.find('#start').prop('disabled', true);
                        self.board.find('#guess').prop('disabled', false);
                        self.updateBoard(res);
                    }
                );
            });

            this.board.on('click', '#guess', function () {
                let code = self.board.find('.guess .answer-cell').map(function () {
                    return $(this).data('color');
                }).get();
                $.ajax({
                    type: "POST",
                    url: self.guessHandlerUrl,
                    dataType: 'json',
                    async: true,
                    headers: {
                        "Content-Type": "application/json"
                    },
                    data: JSON.stringify({code: code}),
                    success: function (res) {
                        self.updateBoard(res);
                        self.checkGameStatus(res);
                        if (!res.isActive) {
                            self.board.find('#start').prop('disabled', false);
                            self.board.find('#guess').prop('disabled', true);
                            self.checkScore(res);
                        }
                    }
                });
            });

            this.pollGame(function (res, status, jqXHR) {
                self.checkScore(res);
            });
        }

        pollGame(onSuccess) {
            $.ajax({
                type: "POST",
                url: this.gameHandlerUrl,
                dataType: 'json',
                async: true,
                headers: {
                    "Content-Type": "application/json"
                },
                success: function (res, status, jqXHR) {
                    onSuccess(res, status, jqXHR);
                }
            });
        }

        checkScore(response) {
            this.board.find('#player-score').text(response.score[0]);
            this.board.find('#computer-score').text(response.score[1]);
        }

        clearBoard() {
            for (let i = 0; i < 12; i++) {
                for (let ii = 0; ii < 4; ii++) {
                    let cell_id = '#answer-cell-' + i + '-' + ii;
                    this.board.find(cell_id).css('background', '#D7D7D7');
                    let position_hint_cell_id = '#hint-cell-' + i + '-' + ii;
                    this.board.find(position_hint_cell_id).css('background', '#D7D7D7');
                }
                let solution_cell_id = '#solution-cell-' + i;
                this.board.find(solution_cell_id).css('background', '#D7D7D7');
            }
        }

        updateBoard(response) {
            for (let i = 0; i < response.guesses.length; i++) {
                let guess = response.guesses[i];
                for (let ii = 0; ii < guess.code.length; ii++) {
                    let cell_id = '#answer-cell-' + i + '-' + ii;
                    this.board.find(cell_id).css('background', guess.code[ii]);
                }
                let [position_ok, color_ok] = guess.hint;
                for (let iii = 0; iii < position_ok; iii++) {
                    let position_hint_cell_id = '#hint-cell-' + i + '-' + iii;
                    this.board.find(position_hint_cell_id).css('background', 'black');
                }
                for (let iv = position_ok; iv < position_ok + color_ok; iv++) {
                    let color_hint_cell_id = '#hint-cell-' + i + '-' + iv;
                    this.board.find(color_hint_cell_id).css('background', 'white');
                }
            }
        }

        checkGameStatus(response) {
            if (response.code) {
                for (let i = 0; i < response.code.length; i++) {
                    let cell_id = '#solution-cell-' + i;
                    this.board.find(cell_id).css('background', response.code[i]);
                }
                if (response.codeBroken) {
                    alert("You guessed the secret!")
                }
                else {
                    alert("Too bad! You have exhausted your guesses")
                }
            }
        }

    }

    $.fn.masterMind = function(settings) {

        let masterMindApi = new MasterMindApi({
            board: $(this),
            colors: settings.colors,
            gameHandlerUrl: settings.gameHandlerUrl
        });
        masterMindApi.init();

        return this;

    };

}( jQuery ));