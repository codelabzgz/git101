// Generate the guide body, retaining the corporate template's header and footer.
const fs = require('node:fs');
const path = require('node:path');
const JSZip = require('jszip');
const {Document, Paragraph, TextRun, PageBreak, Packer, HeadingLevel, Table, TableRow,
       TableCell, WidthType, ShadingType} = require('docx');

async function main() {
  const [template, output] = process.argv.slice(2);
  if (!template || !output) throw Error('Usage: export-guide.cjs template.docx output.docx');
  const text = fs.readFileSync(path.join(__dirname, '../GUION.md'), 'utf8');
  const original = await JSZip.loadAsync(fs.readFileSync(template));
  const xml = await original.file('word/document.xml').async('string');
  const section = xml.match(/<w:sectPr[\s>][\s\S]*?<\/w:sectPr>/)[0];
  const corporateBand = xml.match(/<w:body>\s*(<w:tbl[\s>][\s\S]*?<\/w:tbl>)/)?.[1];
  if (!corporateBand || !corporateBand.includes('w:drawing')) throw Error('Template has no corporate band');
  const page = section.match(/<w:pgSz[^>]*w:w="(\d+)"/);
  const margins = section.match(/<w:pgMar[^>]*>/)[0];
  const left = Number(margins.match(/w:left="(\d+)"/)[1]);
  const right = Number(margins.match(/w:right="(\d+)"/)[1]);
  const width = Number(page[1]) - left - right;
  const paragraphs = [];
  let code = false, tableRows = [], paragraph = [];
  function plain(value, options = {}) {
    return new Paragraph({spacing:{after:100}, ...options,
      children:[new TextRun({text:value, font:'Arial', size:21})]});
  }
  function flushParagraph() {
    if (paragraph.length) paragraphs.push(plain(paragraph.join(' ')));
    paragraph = [];
  }
  function flushTable() {
    if (!tableRows.length) return;
    const cols = tableRows[0].length;
    const widths = Array.from({length:cols},(_,i)=>i === cols-1 ? width - Math.floor(width/cols)*(cols-1) : Math.floor(width/cols));
    const rows = tableRows.map((cells,i)=>new TableRow({tableHeader:i===0, cantSplit:true,
      children:cells.map((value,j)=>new TableCell({width:{size:widths[j],type:WidthType.DXA},
        margins:{top:80,bottom:80,left:100,right:100},
        shading:{fill:i===0?'E8E8FF':'FFFFFF',type:ShadingType.CLEAR},
        children:[plain(value)]}))}));
    paragraphs.push(new Table({width:{size:width,type:WidthType.DXA}, columnWidths:widths,rows}));
    paragraphs.push(plain(''));
    tableRows=[];
  }
  for (const line of text.split(/\r?\n/)) {
    if (line.startsWith('```')) {flushParagraph();flushTable();code=!code;continue;}
    if (code) {
      paragraphs.push(new Paragraph({spacing:{after:0},keepNext:false,
        children:[new TextRun({text:line,font:'Consolas',size:19})]}));
      continue;
    }
    if (line.startsWith('|')) {
      flushParagraph();
      if (!/^\|\s*[-:]+/.test(line)) tableRows.push(line.split('|').slice(1,-1).map(x=>x.trim()));
      continue;
    }
    flushTable();
    const heading = line.match(/^(#{1,3}) (.*)$/);
    if (heading) {
      flushParagraph();
      if (heading[2].startsWith('1. Qué son Git')) paragraphs.push(new Paragraph({children:[new PageBreak()]}));
      paragraphs.push(new Paragraph({heading:heading[1].length===1?HeadingLevel.HEADING_1:HeadingLevel.HEADING_2,
        keepNext:true,pageBreakBefore:heading[2].startsWith('1. Qué son Git'),spacing:{before:240,after:120},
        children:[new TextRun({text:heading[2],font:'Arial',color:'2323C9',bold:true,size:heading[1].length===1?32:25})]}));
    } else if (!line.trim()) flushParagraph();
    else paragraph.push(line.replace(/`([^`]+)`/g,'$1'));
  }
  flushParagraph();flushTable();
  const bodyDoc = new Document({sections:[{properties:{page:{size:{width:11906,height:16838}}},children:paragraphs}]});
  const generated = await JSZip.loadAsync(await Packer.toBuffer(bodyDoc));
  const bodyXml = await generated.file('word/document.xml').async('string');
  const body = bodyXml.match(/<w:body>([\s\S]*)<\/w:body>/)[1].replace(/<w:sectPr[\s>][\s\S]*?<\/w:sectPr>/,'');
  original.file('word/document.xml',xml.replace(/<w:body>[\s\S]*<\/w:body>/,`<w:body>${corporateBand}${body}${section}</w:body>`));
  if (!Object.keys(original.files).some(x=>x.startsWith('word/media/'))) throw Error('Template has no logo');
  fs.writeFileSync(output,await original.generateAsync({type:'nodebuffer'}));
  console.log(output);
}
main().catch(e=>{console.error(e);process.exitCode=1;});
