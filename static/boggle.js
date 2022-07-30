"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure

  let $board = $('.board');
  $board.empty();

  let $body = $('<tbody>')

  for(let row of board) {
    let $bodyRow = $('<tr>');

    for(let cell of row) {
      $bodyRow.append($(`<td>${cell}</td>`))
    }
    $body.append($bodyRow)
  }
  $board.append($body)

}

// I didn't do any functions after this point

async function handleFormSubmit(evt) {
  evt.preventDefault();

  const word = $wordInput.val().toUpperCase();
  if (!word) return;

  await submitWordToAPI(word);

  $wordInput.val("").focus(); // focus will just make the focus go back on this area
}

$form.on("submit", handleFormSubmit);

async function submitWordToAPI(word) {
  const response = await axios({
    url: "/api/score-word",
    method: "POST",
    data: { word, gameId }
  });

  const { result } = response.data;

  if (result === "not-word") {
    showMessage(`Not valid word: ${word}`, "err");
  } else if (result === "not-on-board") {
    showMessage(`Not on board: ${word}`, "err");
  } else {
    showWord(word);
    showMessage(`Added: ${word}`, "ok");
  }
}

function showWord(word) {
  $($playedWords).append($("<li>", { text: word }));
}

function showMessage(msg, cssClass) {
  $message
    .text(msg)
    .removeClass()
    .addClass(`msg ${cssClass}`);
}



start();

/* basically, the code makes a new game instance (axios.post to /api/new-game) and makes the board
with random letters when first entering the page, and then makes it so whenever you submit a word,
it'll await a post request to /api/score-word and put up a message for if it's valid or not.
If it's valid, it'll add the word to the word list

*/