var oApplication=new ActiveXObject("Word.Application");
oApplication.Visible=true; // "Visible" is in the Word Object Model`
oApplication.Documents.Open("myfilename");
var oDocument=oApplication.ActiveDocument;
var oTable=oDocument.Tables(1);`