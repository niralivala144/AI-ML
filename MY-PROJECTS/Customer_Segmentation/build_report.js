const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, ImageRun, AlignmentType, BorderStyle, PageBreak, Header, Footer,
  PageNumber, LevelFormat, convertInchesToTwip
} = require("docx");
const fs = require("fs");

const PURPLE = "6C5CE7";
const DARK = "2D3436";
const GREY = "636E72";

const CHART = (name) => fs.readFileSync(`../outputs/charts/${name}`);

function heading(text, level = HeadingLevel.HEADING_1, color = PURPLE) {
  return new Paragraph({
    heading: level,
    spacing: { before: 320, after: 160 },
    children: [new TextRun({ text, bold: true, color, size: level === HeadingLevel.HEADING_1 ? 30 : 24 })],
  });
}
function body(text) {
  return new Paragraph({ spacing: { after: 160, line: 300 }, children: [new TextRun({ text, size: 22, color: DARK })] });
}
function bullet(text) {
  return new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 90 }, children: [new TextRun({ text, size: 22, color: DARK })] });
}
function image(name, width, height) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 200 }, children: [new ImageRun({ data: CHART(name), transformation: { width, height }, type: "png" })] });
}
function caption(text) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 260 }, children: [new TextRun({ text, italics: true, size: 18, color: GREY })] });
}
function cell(text, opts = {}) {
  return new TableCell({
    width: opts.width ? { size: opts.width, type: WidthType.DXA } : undefined,
    shading: opts.header ? { type: ShadingType.CLEAR, color: "auto", fill: PURPLE } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: opts.header, color: opts.header ? "FFFFFF" : DARK, size: 20 })] })],
  });
}

const personas = [
  { name: "Premium Big Spenders", pct: "20.0%", count: "40", age: "32.9", income: "$86.1k", spend: "81.5" },
  { name: "Careful Affluent", pct: "19.5%", count: "39", age: "39.9", income: "$86.1k", spend: "19.4" },
  { name: "Young Impulsive Spenders", pct: "27.0%", count: "54", age: "25.2", income: "$41.1k", spend: "62.2" },
  { name: "Standard / Average", pct: "23.5%", count: "47", age: "55.6", income: "$54.4k", spend: "48.9" },
  { name: "Budget Conscious", pct: "10.0%", count: "20", age: "46.2", income: "$26.8k", spend: "18.4" },
];
const headerRow = new TableRow({ tableHeader: true, children: ["Segment", "% Base", "Customers", "Avg Age", "Avg Income", "Avg Spend Score"].map((t) => cell(t, { header: true })) });
const dataRows = personas.map((p) => new TableRow({ children: [cell(p.name), cell(p.pct), cell(p.count), cell(p.age), cell(p.income), cell(p.spend)] }));
const personaTable = new Table({ width: { size: 9350, type: WidthType.DXA }, columnWidths: [2400, 1200, 1400, 1250, 1600, 1500], rows: [headerRow, ...dataRows] });

function recRow(seg, goal, actions) {
  return new TableRow({ children: [cell(seg, { width: 2200 }), cell(goal, { width: 3000 }), cell(actions, { width: 4150 })] });
}
const recHeader = new TableRow({ tableHeader: true, children: [cell("Segment", { header: true, width: 2200 }), cell("Strategic Goal", { header: true, width: 3000 }), cell("Recommended Actions", { header: true, width: 4150 })] });
const recTable = new Table({
  width: { size: 9350, type: WidthType.DXA }, columnWidths: [2200, 3000, 4150],
  rows: [
    recHeader,
    recRow("Premium Big Spenders", "Retain & maximize LTV", "VIP experiences, early access to premium collections, personal styling/concierge, high-margin cross-sell."),
    recRow("Careful Affluent", "Unlock spending potential", "High income but low spend — needs trust-building: quality guarantees, premium loyalty perks, curated luxury offers rather than blanket discounts."),
    recRow("Young Impulsive Spenders", "Convert to habitual, higher-value", "Trend-led flash sales, social-media-driven promotions, buy-now-pay-later options, gamified loyalty app."),
    recRow("Standard / Average", "Nurture toward premium", "Mid-tier bundles, seasonal promotions, targeted upsell based on browsing/purchase history."),
    recRow("Budget Conscious", "Efficient value delivery", "Value-pack promotions, essential-item discounts, low-cost loyalty points — avoid deep discounting that erodes margin."),
  ],
});

const doc = new Document({
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.18) } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Mall Customer Segmentation — Analytics Report", size: 16, color: GREY, italics: true })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", size: 16, color: GREY }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GREY })] })] }) },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 80 }, children: [new TextRun({ text: "Mall Customer Segmentation", bold: true, size: 52, color: PURPLE })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: "K-Means Clustering on Age, Income & Spending Behavior", size: 28, color: DARK })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PURPLE, space: 8 } }, spacing: { after: 400 }, children: [new TextRun({ text: "Dataset: Mall_Customers.csv (200 customers)  •  July 2026", size: 20, color: GREY, italics: true })] }),

      heading("Executive Summary", HeadingLevel.HEADING_1),
      body("This analysis segments 200 mall customers using Age, Annual Income, and Spending Score into five distinct behavioral groups via K-Means clustering. The objective is to move marketing spend away from a blanket approach and toward segment-specific strategies that maximize revenue per customer and improve engagement."),
      body("Five well-separated segments emerged (Silhouette Score 0.417), ranging from high-income high-spenders (Premium Big Spenders) to high-income but low-spending customers (Careful Affluent) — a segment with strong untapped revenue potential."),

      heading("Methodology", HeadingLevel.HEADING_1),
      bullet("Data: Mall_Customers.csv — 200 records, no missing values, Age/Gender/Annual Income/Spending Score."),
      bullet("Features used for clustering: Age, Annual Income (k$), Spending Score (1-100)."),
      bullet("Scaling: StandardScaler applied before clustering to normalize feature magnitude."),
      bullet("Model selection: Elbow Method + Silhouette Score used to validate optimal cluster count."),
      bullet("Clustering: K-Means (k=5) — matches the natural income/spending grid pattern in the data."),
      bullet("Visualization: PCA for 2D projection; direct Income-vs-Spending scatter for business interpretability."),
      image("03_optimal_k.png", 520, 320),
      caption("Figure 1 — Elbow Method and Silhouette Score across candidate k values"),

      new Paragraph({ children: [new PageBreak()] }),

      heading("Exploratory Data Analysis", HeadingLevel.HEADING_1),
      body("Age, income, and spending score distributions were examined first, along with gender split and feature correlations, to understand the base before modeling."),
      image("01_eda_distributions.png", 560, 190),
      caption("Figure 2 — Distribution of Age, Annual Income, and Spending Score"),
      image("02b_gender_distribution.png", 320, 260),
      caption("Figure 3 — Gender split (56% Female, 44% Male)"),
      image("02_correlation_heatmap.png", 340, 300),
      caption("Figure 4 — Correlation between Age, Income, and Spending Score"),

      new Paragraph({ children: [new PageBreak()] }),

      heading("The Five Customer Segments", HeadingLevel.HEADING_1),
      body("Each cluster was profiled and mapped to a business-friendly persona for marketing and CRM use."),
      personaTable,
      new Paragraph({ spacing: { before: 240 } }),
      image("04b_income_vs_spending.png", 480, 380),
      caption("Figure 5 — Segments plotted on Income vs Spending Score (most interpretable view)"),
      image("05_segment_sizes.png", 460, 280),
      caption("Figure 6 — Segment size distribution"),
      image("06_radar_profiles.png", 400, 400),
      caption("Figure 7 — Normalized behavioral fingerprint per segment"),

      new Paragraph({ children: [new PageBreak()] }),

      heading("Segment Deep-Dive", HeadingLevel.HEADING_1),
      heading("💎 Premium Big Spenders (20.0%)", HeadingLevel.HEADING_2, PURPLE),
      body("High income (~$86k) and high spending score (~81.5). Youngest of the high-income groups (avg age 33). The most profitable segment — prioritize retention and premium experiences."),
      heading("🏦 Careful Affluent (19.5%)", HeadingLevel.HEADING_2, PURPLE),
      body("Same high income (~$86k) as Premium Big Spenders but very low spending score (~19.4). This is the single highest-opportunity segment — high purchasing power that isn't being converted into spend."),
      heading("⚡ Young Impulsive Spenders (27.0%)", HeadingLevel.HEADING_2, PURPLE),
      body("Youngest segment (avg age 25), moderate income (~$41k) but high spending score (~62.2). Largest segment by size — trend-driven and highly responsive to promotions."),
      heading("📊 Standard / Average (23.5%)", HeadingLevel.HEADING_2, PURPLE),
      body("Oldest segment (avg age 56), mid income (~$54k) and mid spending score (~48.9). Balanced, stable customers with room to grow via targeted upsell."),
      heading("💰 Budget Conscious (10.0%)", HeadingLevel.HEADING_2, PURPLE),
      body("Lowest income (~$27k) and lowest spending score (~18.4). Smallest segment — needs efficient, low-cost engagement rather than heavy investment."),

      heading("Business Recommendations", HeadingLevel.HEADING_1),
      recTable,

      new Paragraph({ spacing: { before: 320 } }),
      heading("Next Steps", HeadingLevel.HEADING_1),
      bullet("Prioritize the 'Careful Affluent' segment — highest untapped revenue potential given their income level."),
      bullet("Operationalize segment labels in CRM for personalized campaigns."),
      bullet("A/B test targeted offers per segment and track lift in spending score / revenue."),
      bullet("Combine with purchase-category data (if available) for deeper personalization."),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Mall_Customer_Segmentation_Report.docx", buf);
  console.log("Report generated.");
});
