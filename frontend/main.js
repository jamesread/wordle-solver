function createLetters (index) {
  const letters = []

  const holder = document.createElement('div')
  holder.setAttribute('data-index', index)

  const lbl = document.createElement('span')
  lbl.classList.add('label')
  lbl.innerText = (index + 1) + ': '
  holder.appendChild(lbl)

  for (let i = 0; i < window.settings.countLetters; i++) {
    const l = document.createElement('span')
    l.classList.add('letter')
    l.innerText = ' '
    l.setAttribute('data-type', 'unused')
    l.onclick = () => {
      if (index === window.currentResultFocus) {
        if (window.currentInputFocus !== i) {
          window.currentInputFocus = i
          refreshLetterCss()

          return
        }

        cycleLetterType(l)
      }
    }

    letters.push(l)

    holder.appendChild(l)
  }

  document.getElementById('letters').append(holder)

  window.letters.push(letters)
}

function cycleLetterType (input) {
  switch (input.getAttribute('data-type')) {
    case 'solved':
      input.setAttribute('data-type', 'unused')
      break
    case 'wrong-position':
      input.setAttribute('data-type', 'solved')
      break
    case 'unused':
      input.setAttribute('data-type', 'wrong-position')
      break
    default:
  }
}

function oninput (e) {
  const input = window.letters[window.currentResultFocus][window.currentInputFocus]

  if (e.key === 'Enter') {
    onInputReq()
    return
  }

  if (e.key === 'ArrowLeft') {
    if (window.currentInputFocus > 0) {
      window.currentInputFocus--
      refreshLetterCss()
      return
    }
  }

  if (e.key === 'ArrowRight') {
    if (window.currentInputFocus + 1 !== window.settings.countLetters) {
      window.currentInputFocus++
      refreshLetterCss()
      return
    }
  }

  if (e.key === 'ArrowDown') {
    cycleLetterType(input)

    return
  }

  console.log(e)

  if (e.key !== ' ' && !/^[a-z]{1}$/i.test(e.key)) {
    return
  }

  input.innerText = e.key.toUpperCase()

  window.currentInputFocus++

  refreshLetterCss()
}

function buildResult () {
  const ret = []

  let i = 0;

  for (const l of window.letters[window.currentResultFocus]) {
    const type = l.getAttribute('data-type')

    if (type === 'solved') {
      window.known[i] = l.innerText
    }


    ret.push({
      character: l.innerText,
      type: type
    })

    i++
  }

  return ret
}

function onInputReq () {
  const payload = {
    result: buildResult()
  }

  const url = window.location.origin + '/enterResult'

  window.fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  }).then((r) => {
    if (r.ok) {
      return r.json()
    } else {
      console.log(r)
      throw new Error('request not OK')
    }
  }).then(j => {
    renderCandidates(j)

    window.currentInputFocus = 0
    window.currentResultFocus++

    prefillKnown()

    refreshLetterCss()
  }).catch(e => {
    console.error(e)
  })
}

function renderCandidates (j) {
  const lbl = document.getElementById('candidates')
  lbl.innerText = ''

  if (j.candidates.length === 0) {
    lbl.innerText = 'NO CANDIATES FOUND!'
  } else {
    lbl.innerText = j.candidates.length + ' CANDIATES FOUND\n\n'

    for (const i in j.candidates) {
      const candidate = j.candidates[i]

      lbl.innerText += i + candidate.ranking + ': ' + candidate.word + '\n'
    }
  }
}

function refreshLetterCss () {
  for (const holder of document.body.querySelectorAll('div')) {
    const index = parseInt(holder.getAttribute('data-index'))

    if (index === window.currentResultFocus) {
      holder.setAttribute('data-state', 'active')
    } else if (index > window.currentResultFocus) {
      holder.setAttribute('data-state', 'pending')
    } else {
      holder.setAttribute('data-state', 'complete')
    }
  }

  for (let resultRow = 0; resultRow < window.settings.countGuesses; resultRow++) {
    const inputs = window.letters[resultRow]

    for (const input of inputs) {
      input.classList.remove('next')

      if (resultRow === window.currentResultFocus) {
        input.classList.add('active-result')
      } else {
        input.classList.remove('active-result')
      }
    }
  }

  if (window.currentInputFocus >= window.settings.countLetters) {
    return
  }

  window.letters[window.currentResultFocus][window.currentInputFocus].classList.add('next')
}

function prefillKnown () {
  for (const pos of Object.keys(window.known)) {
    const l = window.letters[window.currentResultFocus][pos]

    l.innerText = window.known[pos]
    l.setAttribute('data-type', 'solved')
  }
}

function reqReset () {
  window.fetch(window.location.origin + '/reset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  }).catch(e => {
    console.log(e)
  })

  refreshLetterCss()
}

function createResultView () {
  for (let i = 0; i < window.settings.countGuesses; i++) {
    createLetters(i)
  }
}

window.currentInputFocus = 0
window.currentResultFocus = 0
window.letters = []
window.known = {}

function main () {
  createResultView()

  reqReset()

  document.body.addEventListener('keyup', oninput)

  refreshLetterCss()
}

window.settings = {
  countGuesses: 6,
  countLetters: 5
}

main()
