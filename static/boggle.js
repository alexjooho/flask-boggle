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


start();