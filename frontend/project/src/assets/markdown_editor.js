class Compiler {
  constructor() {
    this.tokenHtmlTag = {
      openTag: '<span class="md-token">',
      closeTag: '</span>',
    };
    this.infixFormatters = {
      '**': {openTag: '<strong>', closeTag: '</strong>'},
      '__': {openTag: '<strong>', closeTag: '</strong>'},
      '_': {openTag: '<em>', closeTag: '</em>'},
      '*': {openTag: '<em>', closeTag: '</em>'},
      '~~': {openTag: '<strike>', closeTag: '</strike>'},
      '`': {openTag: '<code>', closeTag: '</code>'},
    };
    this.prefixFormatters = [
      {regex: new RegExp('^# '), openTag: '<h1>', closeTag: '</h1>'},
      {regex: new RegExp('^## '), openTag: '<h2>', closeTag: '</h2>'},
      {regex: new RegExp('^### '), openTag: '<h3>', closeTag: '</h3>'},
      {regex: new RegExp('^#### '), openTag: '<h4>', closeTag: '</h4>'},
      {regex: new RegExp('^##### '), openTag: '<h5>', closeTag: '</h5>'},
      {regex: new RegExp('^###### '), openTag: '<h6>', closeTag: '</h6>'},
      {regex: new RegExp('^> '), openTag: '<blockquote>', closeTag: '</blockquote>'},
      {regex: new RegExp('^- '), openTag: '<li>', closeTag: '</li>'},
      {regex: new RegExp('^\\* '), openTag: '<li>', closeTag: '</li>'},
      {regex: new RegExp('^\\+ '), openTag: '<li>', closeTag: '</li>'},
      {regex: new RegExp('^[0-9]+\\. '), openTag: '<li style="list-style:decimal">', closeTag: '</li>'},
    ];
  }
  compileText(text, startingReferences) {
    const newReferences = startingReferences;
    const paragraphs = this.splitStringToParagraphs(text);
    const compiledElements = [];
    for (const paragraph of paragraphs) {
      const compiled = this.compileParagraph(paragraph, newReferences);
      if (compiled.reference) {
        newReferences[compiled.reference.name] = compiled.reference.data;
        this.fixReferences(compiledElements, compiled.reference);
      }
      if (compiled.html.tagName === 'TABLE' && compiledElements.length > 1 &&
                compiledElements[compiledElements.length - 1].tagName === 'TABLE') {
        this.fixTable(compiled.html, compiledElements[compiledElements.length - 1]);
      } else {
        compiledElements.push(compiled.html);
      }
    }
    return {
      html: compiledElements,
      references: newReferences,
    };
  }
  compileParagraph(paragraph, references) {
    const compiled = this.compilePrefix(paragraph);
    if (compiled.reference) {
      return {
        html: htmlElementFromString('<p>' + compiled.str + '<p>'),
        reference: compiled.reference,
      };
    } else {
      const inlineTokens = this.tokenizeParagraphForInfixCompilation(compiled.str);
      compiled.str = this.compileInfixTokens(inlineTokens);
      compiled.str = this.compileImage(compiled.str, references);
      compiled.str = this.compileLink(compiled.str, references);
      const element = htmlElementFromString(compiled.str);
      element.setAttribute('data-text', paragraph);
      element.classList.add('md');
      return {html: element};
    }
  }
  compileImage(paragraph, references) {
    const imageRegex = /!\[(.*?)\]\((.*?)( "(.*)")?\)/g;
    for (const match of paragraph.matchAll(imageRegex)) {
      const alt = match[1] !== undefined ? match[1] : '';
      const link = match[2] !== undefined ? match[2] : '';
      const title = match[4] !== undefined ? match[4] : '';
      const htmlTag = `<img src="${link}" alt="${alt}" title="${title}" class="md">`;
      paragraph = paragraph.replace(match[0], htmlTag);
    }
    const imageReferenceRegex = /!\[(.*?)\](\[(.*?)\])?/g;
    for (const match of paragraph.matchAll(imageReferenceRegex)) {
      const alt = match[1] !== undefined ? match[1] : '';
      const ref = match[3] !== undefined ? match[3] : '';
      let link = '';
      let title = '';
      if (references[ref] !== undefined) {
        link = references[ref].link !== undefined ? references[ref].link : '';
        title = references[ref].title !== undefined ? references[ref].title : '';
      }
      const htmlTag = `<img src="${link}" alt="${alt}" title="${title}" data-reference="${ref}" class="md">`;
      paragraph = paragraph.replace(match[0], htmlTag);
    }
    return paragraph;
  }
  compileLink(paragraph, references) {
    const linkRegex = /\[(.*?)\](\((.*?)( "(.*)")?\)|\[(.*)\])?/g;
    for (const match of paragraph.matchAll(linkRegex)) {
      let htmlTag = match[0];
      const name = match[1] !== undefined ? match[1] : '';
      let link = match[3] !== undefined ? match[3] : '';
      let title = match[5] !== undefined ? match[5] : '';
      let ref = match[6] !== undefined ? match[6] : '';
      if (match[2] && match[2].startsWith('(')) {
        htmlTag = `<a href="${link}" title="${title}" class="md">${name}</a>`;
      } else {
        if (match[2] === undefined) {
          ref = name;
        }
        if (references[ref] !== undefined) {
          link = references[ref].link !== undefined ? references[ref].link : '';
          title = references[ref].title !== undefined ? references[ref].title : '';
        }
        htmlTag = `<a href="${link}" title="${title}" data-reference="${ref}" class="md">${name}</a>`;
      }
      paragraph = paragraph.replace(match[0], htmlTag);
    }
    return paragraph;
  }
  compileTable(paragraph) {
    paragraph = paragraph.trim();
    if (paragraph[0] === '|') {
      paragraph = paragraph.substr(1);
    }
    if (paragraph[paragraph.length - 1] === '|') {
      paragraph = paragraph.substr(0, paragraph.length - 2);
    }
    paragraph = '<table class="md"><tr><td class="md" >' + paragraph + '</td></tr></table>';
    paragraph = paragraph.replace(/\|/g, '</td><td class="md">');
    return paragraph;
  }
  tokenizeParagraphForInfixCompilation(paragraph) {
    if (/^```/.test(paragraph)) {
      return [paragraph];
    }
    const tokens = [];
    const addDoubleToken = (char) => {
      if (tokens[tokens.length - 1] === char) {
        tokens[tokens.length - 1] = char.repeat(2);
      } else {
        tokens.push(char);
      }
    };
    if (/^<li>\* /.test(paragraph)) {
      paragraph = paragraph.substr(6);
      tokens.push('<li>* ');
    }
    for (const char of paragraph) {
      if (tokens.length === 0) {
        tokens.push(char);
        continue;
      }
      if (char === '*' || char === '_' || char === '~') {
        addDoubleToken(char);
      } else if (char === '`') {
        tokens.push(char);
      } else {
        if (this.infixFormatters[tokens[tokens.length - 1]] !== undefined) {
          tokens.push(char);
        } else {
          tokens[tokens.length - 1] = tokens[tokens.length - 1].concat(char);
        }
      }
    }
    return tokens;
  }
  compileInfixTokens(tokens) {
    let compiled = '';
    const formatTokenSet = new Set();
    for (const token of tokens) {
      if (this.infixFormatters[token] !== undefined) {
        if (!formatTokenSet.has(token)) {
          formatTokenSet.add(token);
          compiled = compiled +
                        this.infixFormatters[token].openTag + this.tokenHtmlTag.openTag + token +
                        this.tokenHtmlTag.closeTag;
        } else {
          formatTokenSet.delete(token);
          compiled = compiled + this.tokenHtmlTag.openTag + token + this.tokenHtmlTag.closeTag +
                        this.infixFormatters[token].closeTag;
        }
      } else {
        compiled = compiled + token;
      }
    }
    return compiled;
  }
  compilePrefix(paragraph) {
    for (const prefix of this.prefixFormatters) {
      if (prefix.regex.test(paragraph)) {
        const prefixMatch = paragraph.match(prefix.regex);
        if (prefixMatch) {
          const prefixString = prefixMatch[0];
          const paragraphWithoutPrefixFormatter = paragraph.substr(prefixString.length);
          const paragraphContent = this.tokenHtmlTag.openTag + prefixString + this.tokenHtmlTag.closeTag +
                        paragraphWithoutPrefixFormatter;
          return {str: prefix.openTag + paragraphContent + prefix.closeTag};
        }
      }
    }
    if (paragraph.startsWith('```')) {
      paragraph = paragraph.replace('```', '');
      paragraph = paragraph.replace('```', '');
      const languageMatch = paragraph.match(/^(.*)\n/);
      let language = 'js';
      if (languageMatch && languageMatch[1]) {
        language = languageMatch[1];
      }
      paragraph = paragraph.replace(/.*\n/, '');
      return {str: `<pre><code class="language-${language}">` + paragraph + '</code></pre>',
      };
    }
    if (paragraph.includes('|')) {
      return {str: this.compileTable(paragraph)};
    }
    if (/^(-{3,}|\*{3,}|_{3,})$/.test(paragraph)) {
      return {str: '<hr/>'};
    }
    if (/^\[.*?\]:/.test(paragraph)) {
      const anchorRegex = /^\[(.*)\]:\s*([^"]*)(\s)?("(.*)")?/;
      const anchorParts = paragraph.match(anchorRegex);
      if (anchorParts && anchorParts[1] !== undefined) {
        return {
          str: paragraph,
          reference: {
            name: anchorParts[1],
            data: {
              link: anchorParts[2] !== undefined ? anchorParts[2] : '',
              title: anchorParts[5] !== undefined ? anchorParts[5] : '',
            },
          },
        };
      }
    }
    return {str: '<p>' + paragraph + '</p>'};
  }
  fixReferences(elements, reference) {
    elements.map((element) => element.querySelectorAll(`[data-reference="${reference.name}"]`))
        .map((nodes) => {
          for (const node of nodes) {
            node.setAttribute('title', reference.data.title);
            if (node.tagName === 'A') {
              node.setAttribute('href', reference.data.link);
            } else if (node.tagName === 'IMG') {
              node.setAttribute('src', reference.data.link);
            }
          }
        });
  }
  fixTable(currentElement, prevSibling, nextSibling) {
    if (currentElement.tagName !== 'TABLE') {
      return;
    }
    if (prevSibling && prevSibling.nodeName === 'TABLE') {
      for (const row of currentElement.childNodes) {
        const trElement = row;
        prevSibling.appendChild(trElement);
      }
      if (currentElement.parentElement) {
        currentElement.parentElement.removeChild(currentElement);
      }
      currentElement = prevSibling;
    }
    if (nextSibling && nextSibling.nodeName === 'TABLE') {
      for (const row of nextSibling.childNodes) {
        const trElement = row;
        currentElement.appendChild(trElement);
      }
      if (nextSibling.parentElement) {
        nextSibling.parentElement.removeChild(nextSibling);
      }
    }
  }
  splitStringToParagraphs(text) {
    const lines = text.split('\n');
    const paragraphs = [];
    let paragraphBuffer = '';
    const appendBuffer = () => {
      if (paragraphBuffer.length != 0) {
        paragraphs.push(paragraphBuffer);
        paragraphBuffer = '';
      }
    };
    const specialParagraphStart = /^(#{1,6} |\d+\. |\* |\+ |- |> )/;
    const horizontalLine = /^(-{3,}|\*{3,}|_{3,})$/;
    const anchor = /^\[.+\]:/;
    const code = /^```/;
    let insideCodeBlock = false;
    for (const line of lines) {
      if (code.test(line)) {
        paragraphBuffer += line;
        if (insideCodeBlock) {
          appendBuffer();
        } else {
          paragraphBuffer += '\n';
        }
        insideCodeBlock = !insideCodeBlock;
        continue;
      }
      if (insideCodeBlock) {
        paragraphBuffer += line + '\n';
        continue;
      }
      if (specialParagraphStart.test(line) || horizontalLine.test(line) ||
                anchor.test(line) || line.includes('|')) {
        appendBuffer();
        paragraphs.push(line);
      } else if (line.trim() === '') {
        appendBuffer();
      } else {
        paragraphBuffer = paragraphBuffer.concat(line);
      }
    }
    appendBuffer();
    return paragraphs;
  }
}
class CssInjector {
  constructor() {
    CssInjector.styleElement = document.createElement('style');
    CssInjector.styleElement.type = 'text/css';
    document
        .getElementsByTagName('head')[0]
        .appendChild(CssInjector.styleElement);
  }
  static injectCss(identifier, properties) {
    if (properties === this.cssRules[identifier]) {
      return;
    }
    this.cssRules[identifier] = properties;
    let css = '';
    Object.keys(this.cssRules).map((key) => {
      const cssTextPropertoes = CssInjector.stringifyCSSProperties(this.cssRules[key]);
      css += `${key} { ${cssTextPropertoes} } \n`;
    });
    this.styleElement.innerHTML = css;
  }
  static stringifyCSSProperties(property) {
    let cssString = '';
    Object.entries(property).forEach(([key, value]) => {
      if (value !== '') {
        cssString += `${key}: ${value}; `;
      }
    });
    return cssString;
  }
}
CssInjector.cssRules = {};
CssInjector.instance = new CssInjector();
class CssRules {
  constructor() {
    this.rules = {};
  }
}


class Editor {
  constructor(wrapperId, formatter, theme, view_only_input) {
    this.formatter = formatter;
    this.theme = theme;
    this.wrapper = document.createElement('div');
    this.editor = document.createElement('div');
    this.menu = document.createElement('div');
    this.view_only = view_only_input;
    console.log(this.view_only, view_only_input);
    this.idPrefix = wrapperId;
    this.initializeWrapper(this.idPrefix);
    this.applyTheme();
    this.formatter.init(this.editor);
  }
  setContent(content) {
    this.formatter.setContent(content);
  }
  setContentBasic()
  {
    this.formatter.setContentBasic();
  }
  getContent() {
    return this.formatter.getContent();
  }
  injectAdditionalCssRules() {
    if (this.theme.additionalCssRules) {
      Object.entries(this.theme.additionalCssRules.rules).forEach(([identifier, properties]) => {
        CssInjector.injectCss(identifier, properties);
      });
    }
  }
  injectScrollbarTheme() {
    if (this.theme.scrollbarTheme) {
      Object.entries(this.theme.scrollbarTheme).forEach(([identifier, properties]) => {
        const cssIdentifier = '#' + this.getEditorId() + '::' + identifier;
        CssInjector.injectCss(cssIdentifier, properties);
      });
    }
  }
  createWrapperId() {
    this.wrapper.id = this.idPrefix;
    this.wrapper.id = this.getWrapperId();
  }
  createWrapper(futureWrapperId) {
    const futureWrapper = document.getElementById(futureWrapperId);
    if (!futureWrapper) {
      throw new Error('Cannot find element with id ' + futureWrapperId);
    }
    const futureWrapperParent = futureWrapper.parentElement;
    if (!futureWrapperParent) {
      throw new Error('Cannot find parent of element with id ' + futureWrapperId);
    }
    this.createWrapperId();
    futureWrapperParent.replaceChild(this.wrapper, futureWrapper);
  }
  createMenu() {
    if (this.view_only === false) {
      this.createMenuBase();
      this.createMenuSettingsItems();
    }
  }
  createMenuBase() {
    this.wrapper.appendChild(this.menu);
    this.menu.id = this.getMenuId();
    const settingsSvg = htmlElementFromString(`
        <div style='display: flex; justify-content: flex-end;'>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6" />
          </svg>
          <svg display='none' width="24" height="24" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </div>`);
    this.menu.appendChild(settingsSvg);
    settingsSvg.addEventListener('click', (event) => {
      this.settingsClick(event, this.menu);
    });
  }
  createMenuSettingsItems() {
    const settingsWrapper = document.createElement('div');
    this.menu.appendChild(settingsWrapper);
    settingsWrapper.style.display = 'none';
    settingsWrapper.style.flexDirection = 'column';
    this.formatter
        .getSettings()
        .forEach((element) => settingsWrapper.appendChild(element));
  }
  createEditor() {
    this.wrapper.appendChild(this.editor);
    this.editor.id = this.getEditorId();   
    if(this.view_only){
      this.editor.contentEditable = 'false';
    }
    else{
      this.editor.contentEditable = 'true';
    }
  }
  initializeWrapper(futureWrapperId) {
    this.createWrapper(futureWrapperId);
    this.createMenu();
    this.createEditor();
  }
  settingsClick(event, menu) {
    const target = event.currentTarget;
    if (target.parentElement) {
      const svgs = target.children;
      for (const svg of svgs) {
        if (svg.hasAttribute('display')) {
          svg.removeAttribute('display');
        } else {
          svg.setAttribute('display', 'none');
        }
      }
      if (target.parentElement.style.width === '') {
        target.parentElement.style.width = '10em';
        menu.children[1].style.display = 'flex';
      } else {
        target.parentElement.style.width = '';
        menu.children[1].style.display = 'none';
      }
    }
  }
  applyTheme() {
    this.injectWrapperTheme();
    this.injectMenuCss();
    this.injectEditorCss();
    this.injectScrollbarTheme();
    this.injectAdditionalCssRules();
  }
  injectEditorCss() {
    CssInjector.injectCss(this.getEditorIdentifier(), this.getEditorBaseCssProperties());
  }
  injectMenuCss() {
    CssInjector.injectCss(this.getMenuIdentifier(), this.getMenuBaseCssProperties());
  }
  injectWrapperTheme() {
    const wrapperCss = this.getWrapperCssProperties();
    CssInjector.injectCss(this.getWrapperIdentifier(), wrapperCss);
  }
  getWrapperCssProperties() {
    if (this.theme.editorTheme) {
      return {
        ...this.getWrapperBaseCssProperties(),
        ...this.theme.editorTheme,
      };
    }
    return this.getWrapperBaseCssProperties();
  }
  getWrapperBaseCssProperties() {
    return {
      'cursor': 'default',
      'display': 'flex',
      'flex-direction': 'row',
      'resize': 'none',
      'overflow': 'auto',
    };
  }
  getMenuBaseCssProperties() {
    return {
      'border-right': '1px solid rgb(83, 79, 86)',
      'margin': '20px 0px 20px 0px',
      'padding': '15px 20px 15px 20px',
      'display': 'flex',
      'flex-direction': 'column',
    };
  }
  getEditorBaseCssProperties() {
    return {
      'flex': '1',
      'outline': 'none',
      'overflow': 'auto',
      'scrollbar-color': 'red',
      'padding': '20px 30px 20px 30px',
      'margin': '10px 10px 10px 10px',
    };
  }
  getWrapperIdentifier() {
    return '#' + this.getWrapperId();
  }
  getMenuIdentifier() {
    return '#' + this.getMenuId();
  }
  getEditorIdentifier() {
    return '#' + this.getEditorId();
  }
  getWrapperId() {
    return this.idPrefix + '-wrapper';
  }
  getMenuId() {
    return this.idPrefix + '-menu';
  }
  getEditorId() {
    return this.idPrefix + '-editor';
  }
}
class Formatter {
}
function htmlElementFromString(html) {
  const creationHelperElement = document.createElement('div');
  creationHelperElement.innerHTML = html.trim();
  if (creationHelperElement.firstChild &&
        creationHelperElement.firstChild.nodeType === Node.ELEMENT_NODE) {
    return creationHelperElement.firstChild;
  }
  throw new Error('Failed to create element from html: ' + html);
}
let SpecialKey;
(function(SpecialKey) {
  SpecialKey[SpecialKey['esc'] = 27] = 'esc';
  SpecialKey[SpecialKey['tab'] = 9] = 'tab';
  SpecialKey[SpecialKey['space'] = 32] = 'space';
  SpecialKey[SpecialKey['return'] = 13] = 'return';
  SpecialKey[SpecialKey['enter'] = 13] = 'enter';
  SpecialKey[SpecialKey['backspace'] = 8] = 'backspace';
  SpecialKey[SpecialKey['scrollLock'] = 145] = 'scrollLock';
  SpecialKey[SpecialKey['capsLock'] = 20] = 'capsLock';
  SpecialKey[SpecialKey['numLock'] = 144] = 'numLock';
  SpecialKey[SpecialKey['pause'] = 19] = 'pause';
  SpecialKey[SpecialKey['insert'] = 45] = 'insert';
  SpecialKey[SpecialKey['home'] = 36] = 'home';
  SpecialKey[SpecialKey['delete'] = 46] = 'delete';
  SpecialKey[SpecialKey['end'] = 35] = 'end';
  SpecialKey[SpecialKey['pageUp'] = 33] = 'pageUp';
  SpecialKey[SpecialKey['pageDown'] = 34] = 'pageDown';
  SpecialKey[SpecialKey['left'] = 37] = 'left';
  SpecialKey[SpecialKey['up'] = 38] = 'up';
  SpecialKey[SpecialKey['right'] = 39] = 'right';
  SpecialKey[SpecialKey['down'] = 40] = 'down';
  SpecialKey[SpecialKey['f1'] = 112] = 'f1';
  SpecialKey[SpecialKey['f2'] = 113] = 'f2';
  SpecialKey[SpecialKey['f3'] = 114] = 'f3';
  SpecialKey[SpecialKey['f4'] = 115] = 'f4';
  SpecialKey[SpecialKey['f5'] = 116] = 'f5';
  SpecialKey[SpecialKey['f6'] = 117] = 'f6';
  SpecialKey[SpecialKey['f7'] = 118] = 'f7';
  SpecialKey[SpecialKey['f8'] = 119] = 'f8';
  SpecialKey[SpecialKey['f9'] = 120] = 'f9';
  SpecialKey[SpecialKey['f10'] = 121] = 'f10';
  SpecialKey[SpecialKey['f11'] = 122] = 'f11';
  SpecialKey[SpecialKey['f12'] = 123] = 'f12';
})(SpecialKey || (SpecialKey = {}));

let MdCss;
(function(MdCss) {
  MdCss['global'] = '*.md';
  MdCss['paragraph'] = 'p.md';
  MdCss['header1'] = 'h1.md';
  MdCss['header2'] = 'h2.md';
  MdCss['header3'] = 'h3.md';
  MdCss['header4'] = 'h4.md';
  MdCss['header5'] = 'h5.md';
  MdCss['header6'] = 'h6.md';
  MdCss['italics'] = 'em.md';
  MdCss['bold'] = 'strong.md';
  MdCss['strikethrough'] = 'strike.md';
  MdCss['orderedList'] = 'ol.md';
  MdCss['unorderedList'] = 'ul.md';
  MdCss['link'] = 'a.md';
  MdCss['image'] = 'img.md';
  MdCss['inlineCode'] = 'code.md';
  MdCss['blockCode'] = 'pre.md';
  MdCss['table'] = 'table.md';
  MdCss['tableHeader'] = 'th.md';
  MdCss['tableCell'] = 'td.md';
  MdCss['quote'] = 'blockquote.md';
  MdCss['horizontalLine'] = 'hr.md';
})(MdCss || (MdCss = {}));
class MdCssRules extends CssRules {
  constructor() {
    super(...arguments);
    this.rules = {
      '*.md': {},
      'p.md': {},
      'h1.md': {},
      'h2.md': {},
      'h3.md': {},
      'h4.md': {},
      'h5.md': {},
      'h6.md': {},
      'em.md': {},
      'strong.md': {},
      'strike.md': {},
      'ol.md': {},
      'ul.md': {},
      'a.md': {},
      'img.md': {},
      'code.md': {},
      'pre.md': {},
      'table.md': {},
      'th.md': {},
      'td.md': {},
      'blockquote.md': {},
      'hr.md': {},
    };
  }
}


class MdFormatter extends Formatter {
  constructor(view_only) {
    super(...arguments);
    this.editor = document.createElement('invalid');
    this.view_only = view_only;
    this.settings = {
      dynamicRender: false,
      showSyntax: false,
    };
    this.documentData = {
      currentParagraph: null,
      references: {},
    };
    this.compiler = new Compiler();
  }
  init(editor) {
    this.editor = editor;
    //this.initMutationListeners();
    //this.initKeyboardEventListeners();
    //this.initMouseEventListeners();
    CssInjector.injectCss('.md-token', {
      display: 'none',
    });
  }
  setContent(content) {
    const {html, references} = this.compiler.compileText(content, {});
    this.editor.innerHTML = '';
    for (const element of html) {
      this.editor.appendChild(element);
    }
    this.documentData.references = references;
    Prism.highlightAll();
  }
  setContentBasic()
  {
    const newParagraphs = [];
    for (const paragraph of this.editor.childNodes) {
      const element = paragraph;
      const p = document.createElement('p');
      if (element.hasAttribute('data-text')) {
        const text = element.getAttribute('data-text');
        if (text) {
          p.innerText = text;
        }
      } else {
        p.innerText = element.innerText;
      }
      newParagraphs.push(p);
    }
    this.editor.innerHTML = '';
    for (const element of newParagraphs) {
      this.editor.appendChild(element);
    }
  }
  getContent() {
    let content = '';
    for (const paragraph of this.editor.childNodes) {
      const element = paragraph;
      if (element.hasAttribute('data-text')) {
        content += element.getAttribute('data-text');
      } else {
        content += element.innerText;
      }
      content += '\n\n';
    }
    return content;
  }
  /*
  initMutationListeners() {
    const observerConfig = {
      childList: true,
      subtree: true,
      characterData: true,
    };
    const observer = new MutationObserver((mutations) => this.handleMutations(mutations));
    observer.observe(this.editor, observerConfig);
  }
  initKeyboardEventListeners() {
    this.editor.addEventListener('keyup', () => this.handleKeyUp());
  }
  initMouseEventListeners() {
    this.editor.addEventListener('click', () => this.handleClick());
  }
  handleKeyUp() {
    this.caretMoved();
  }
  */
  getCaretDiv() {
    let element = document.getSelection()?.anchorNode
            ?.parentElement;
    if (element) {
      while (element.parentElement && element.parentElement !== this.editor) {
        element = element.parentElement;
      }
    }
    if (element.parentElement === this.editor) {
      return element;
    } else {
      return null;
    }
  }
  compileCurrentParagraph() {
    if (this.documentData.currentParagraph) {
      this.documentData.currentParagraph.setAttribute('data-text', this.documentData.currentParagraph.innerText);
      const compiled = this.compiler.compileParagraph(this.documentData.currentParagraph.innerText, this.documentData.references);
            this.documentData.currentParagraph.parentElement?.replaceChild(compiled.html, this.documentData.currentParagraph);
            this.documentData.currentParagraph = compiled.html;
            Prism.highlightAll();
            if (compiled.reference) {
              this.documentData.references[compiled.reference.name] = compiled.reference.data;
              this.compiler.fixReferences([this.editor], compiled.reference);
            }
            if (compiled.html.tagName === 'TABLE') {
              this.compiler.fixTable(compiled.html, compiled.html.previousSibling, compiled.html.nextSibling);
            }
    }
  }
  decompileCurrentParagraph(caretPosition) {
    if (this.documentData.currentParagraph) {
      const text = this.documentData.currentParagraph.getAttribute('data-text');
      this.documentData.currentParagraph.removeAttribute('data-text');
      if (text) {
        this.documentData.currentParagraph.innerText = text;
      }
      this.setCaretCharacterOffsetWithin(this.documentData.currentParagraph, caretPosition);
    }
  }
  caretMoved() {
    const newCurrentParagraph = this.getCaretDiv();
    if (this.documentData.currentParagraph !== newCurrentParagraph) {
      let caretPosition = 0;
      if (newCurrentParagraph) {
        caretPosition = this.getCaretCharacterOffsetWithin(newCurrentParagraph);
      }
      if (this.settings.dynamicRender) {
        this.compileCurrentParagraph();
        this.documentData.currentParagraph = newCurrentParagraph;
        this.decompileCurrentParagraph(caretPosition);
      } else {
        this.documentData.currentParagraph = newCurrentParagraph;
      }
    }
  }
  getCaretCharacterOffsetWithin(element) {
    if (!element) {
      return -1;
    }
    let caretOffset = 0;
    const win = window;
    const sel = win.getSelection();
    if (sel && sel.rangeCount > 0) {
      const range = sel.getRangeAt(0);
      const preCaretRange = range.cloneRange();
      preCaretRange.selectNodeContents(element);
      preCaretRange.setEnd(range.endContainer, range.endOffset);
      caretOffset = preCaretRange.toString().length;
    }
    return caretOffset;
  }
  setCaretCharacterOffsetWithin(element, offset) {
    const createRange = (node, offset, range) => {
      if (!range) {
        range = document.createRange();
        range.selectNode(node);
        range.setStart(node, 0);
      }
      if (offset === 0) {
        range.setEnd(node, offset);
      } else if (node && offset > 0) {
        if (node.nodeType === Node.TEXT_NODE) {
          if (node.textContent && node.textContent.length < offset) {
            offset -= node.textContent.length;
          } else {
            range.setEnd(node, offset);
            offset = 0;
          }
        } else {
          for (let lp = 0; lp < node.childNodes.length; lp++) {
            range = createRange(node.childNodes[lp], offset, range);
            if (offset === 0) {
              break;
            }
          }
        }
      }
      return range;
    };
    if (offset >= 0) {
      const selection = window.getSelection();
      const range = createRange(element, offset, null);
      if (range && selection) {
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    }
  }
  handleClick() {
    this.caretMoved();
  }
  getSettings() {
    const settingsHtml = [
      `
      <div data-setting="dynamic-render" style='display: flex;
      flex-direction: row; justify-items: center;
      justify-content: space-between; margin-top: 20px;'>
        <div style='display: flex;'>
          Преглед
        </div>
        <div style='display: flex;'>
          <svg width="24" height="24" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="3"
          stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          </svg>
          <svg display = "none" width="24" height="24" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="3"
            stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 11 12 14 22 4" />
            <path
            d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
          </svg>
        </div>
      </div>
      `,

    ];
    const settingsElements = settingsHtml.map((setting) => htmlElementFromString(setting));
    settingsElements.forEach((element) => {
      if (element.hasAttribute('data-setting')) {
        if (element.getAttribute('data-setting') === 'dynamic-render') {
          element.addEventListener('click', (event) => this.toggleDynamicRender(event));
        } else if (element.getAttribute('data-setting') === 'hide-syntax') {
          element.addEventListener('click', (event) => this.toggleHideSyntax(event));
        }
      }
    });
    return settingsElements;
  }
  toggleDynamicRender(event) {

    const settingsItem = event.currentTarget;
    const svgs = settingsItem?.children[1].children;
    for (const svg of svgs) {
      if (svg.hasAttribute('display')) {
        svg.removeAttribute('display');
      } else {
        svg.setAttribute('display', 'none');
      }
    }
    this.settings.dynamicRender = !this.settings.dynamicRender;

    if (this.settings.dynamicRender) {
      this.editor.contentEditable = 'false';
    }
    else {
      if(this.view_only === false){
      this.editor.contentEditable = 'true';
      }
    }
    console.log(this.editor.contentEditable);
    console.log(this.view_only)

    if (this.settings.dynamicRender) {
      this.setContent(this.getContent());
    } else {
      const newParagraphs = [];
      for (const paragraph of this.editor.childNodes) {
        const element = paragraph;
        const p = document.createElement('p');
        if (element.hasAttribute('data-text')) {
          const text = element.getAttribute('data-text');
          if (text) {
            p.innerText = text;
          }
        } else {
          p.innerText = element.innerText;
        }
        newParagraphs.push(p);
      }
      this.editor.innerHTML = '';
      for (const element of newParagraphs) {
        this.editor.appendChild(element);
      }
    }
  }
  toggleHideSyntax(event) {
    const settingsItem = event.currentTarget;
    const svgs = settingsItem?.children[1].children;
    for (const svg of svgs) {
      if (svg.hasAttribute('display')) {
        svg.removeAttribute('display');
      } else {
        svg.setAttribute('display', 'none');
      }
    }
    this.settings.showSyntax = !this.settings.showSyntax;
    if (this.settings.showSyntax) {
      CssInjector.injectCss('.md-token', {
        display: '',
      });
    } else {
      CssInjector.injectCss('.md-token', {
        display: 'none',
      });
    }
  }
  handleMutations(mutations) {
    mutations.map((mutation) => {
      if (mutation.type === 'childList') {
        this.handleChildListMutation(mutation);
      } else if (mutation.type === 'characterData') {
      }
    });
  }
  handleChildListMutation(mutation) {
    if (mutation.addedNodes.length === 0) {
      return;
    }
    const addedNode = mutation.addedNodes[0];
    if (addedNode.nodeName === '#text' &&
            addedNode.parentElement === this.editor) {
      const newDiv = document.createElement('div');
      this.editor.insertBefore(newDiv, addedNode.nextSibling);
      newDiv.appendChild(addedNode);
      this.documentData.currentParagraph = newDiv;
      const range = document.createRange();
      const sel = window.getSelection();
      range.setStart(this.editor.childNodes[0], newDiv.innerText.length);
      range.collapse(true);
      if (sel) {
        sel.removeAllRanges();
        sel.addRange(range);
      }
    } else if (addedNode.nodeName === '#text') {
      if (addedNode.nodeValue) {
        const currentText = mutation.target.getAttribute('data-text');
        if (currentText) {
          mutation.target.setAttribute('data-text', currentText + addedNode.nodeValue);
        }
      }
    }
  }
}


const darkMDFormatterTheme = new MdCssRules();
darkMDFormatterTheme.rules[MdCss.global] = {
  'font-family': 'sans-serif',
};
darkMDFormatterTheme.rules[MdCss.paragraph] = {
  'font-size': '1em',
};
darkMDFormatterTheme.rules[MdCss.header1] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'font-size': '2em',
  'padding-bottom': '.3em',
  'border-bottom': '1px solid #eaecef',
};
darkMDFormatterTheme.rules[MdCss.header2] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'padding-bottom': '.3em',
  'border-bottom': '1px solid #eaecef',
  'font-size': '1.5em',
};
darkMDFormatterTheme.rules[MdCss.header3] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'font-size': '1.25em',
};
darkMDFormatterTheme.rules[MdCss.header4] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'font-size': '1em',
};
darkMDFormatterTheme.rules[MdCss.header5] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'font-size': '.875em',
};
darkMDFormatterTheme.rules[MdCss.header6] = {
  'margin': '24px 0 16px 0',
  'font-weight': 'bold',
  'line-height': '1.25',
  'font-size': '.85em',
};
darkMDFormatterTheme.rules[MdCss.italics] = {
  'font-style': 'italic',
};
darkMDFormatterTheme.rules[MdCss.bold] = {
  'font-weight': 'bold',
};
darkMDFormatterTheme.rules[MdCss.strikethrough] = {
  'text-decoration': 'line-through',
};
darkMDFormatterTheme.rules[MdCss.orderedList] = {
  'list-style-type': 'decimal',
};
darkMDFormatterTheme.rules[MdCss.unorderedList] = {
  'list-style-type': 'circle',
};
darkMDFormatterTheme.rules[MdCss.link] = {
  'text-decoration': 'none',
  'color': 'rgb(77, 172, 253)',
};
darkMDFormatterTheme.rules[MdCss.image] = {
  'max-width': '90%',
};
darkMDFormatterTheme.rules[MdCss.inlineCode] = {
  'font-family': 'monospace',
  'padding': '.2em .4em',
  'font-size': '85%',
  'border-radius': '3px',
  'background-color': 'rgba(220, 224, 228, 0.1) !important',
};
darkMDFormatterTheme.rules[MdCss.blockCode] = {
  'font-family': 'monospace',
  'border-radius': '3px',
  'word-wrap': 'normal',
  'padding': '16px',
  'background': 'rgba(220, 224, 228, 0.1) !important',
};
darkMDFormatterTheme.rules[MdCss.table] = {
  'color': 'white',
  'border-collapse': 'collapse',
  'width': '100%',
};
darkMDFormatterTheme.rules[MdCss.tableHeader] = {
  'line-height': '1.5',
  'border-spacing': '0',
  'border-collapse': 'collapse',
  'text-align': 'center',
  'font-weight': 'bold',
  'padding': '6px 13px',
  'border': '1px solid white',
};
darkMDFormatterTheme.rules[MdCss.tableCell] = {
  'line-height': '1.5',
  'border-spacing': '0',
  'border-collapse': 'collapse',
  'border': '1px solid white',
  'text-align': 'left',
  'padding': '6px 13px',
};
darkMDFormatterTheme.rules[MdCss.quote] = {
  'border-spacing': '0',
  'border-collapse': 'collapse',
  'padding': '6px 13px',
  'border-left': '.25em solid rgb(53, 59, 66)',
};
darkMDFormatterTheme.rules[MdCss.horizontalLine] = {
  'line-height': '1.5',
  'overflow': 'hidden',
  'height': '.25em',
  'padding': '0',
  'margin': '24px 0',
  'background': 'white',
};
const darkScrollbar = {
  '-webkit-scrollbar': {
    width: '10px',
  },
  '-webkit-scrollbar-track': {
    'background': 'rgb(53, 59, 66)',
    'border-radius': '4px',
  },
  '-webkit-scrollbar-thumb': {
    'background': 'rgb(83, 79, 86)',
    'border-radius': '4px',
  },
  '-webkit-scrollbar-thumb:hover': {
    background: 'rgb(93, 99, 106)',
  },
};
const darkEditorTheme = {
  'background': '#202225',
  'color': '#dcddde',
  'height': '100%',
  'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
};
const sampleMarkdownText = `
\`\`\`javascript
var s = "JavaScript syntax highlighting";
alert( s );
\`\`\`

# Test

1. Test item

2. Test item 2

3. Test item 3

- Unordered test item

- Unordered test item

- Unordered test item
`;
const customTheme = {
  scrollbarTheme: darkScrollbar,
  additionalCssRules: darkMDFormatterTheme,
  editorTheme: darkEditorTheme,
};
