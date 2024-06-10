import { Document, PDFDownloadLink, Page, Canvas } from "@react-pdf/renderer";


const MyDoc = ({component}) => (
  <Document>
    <Page>
      <Canvas />
      {component}
    </Page>
  </Document>
);

const PDFDown = ({component}) => {
    console.log("Cmponent", component);
    return (
      <div>
        <PDFDownloadLink document={<MyDoc component={component}/>} fileName="somename.pdf">
          {({ blob, url, loading, error }) =>
            loading ? 'Loading document...' : 'Download now!'
          }
        </PDFDownloadLink>
      </div>
    )
  };

export default PDFDown;
