// pages/[slug].js
import Head from 'next/head';

export async function getStaticPaths() {
  return {
    paths: [], // no static paths prebuilt
    fallback: 'blocking', // generate on demand
  };
}

export async function getStaticProps({ params }) {
  const slug = params.slug || 'default';
  const [niche, country] = slug.split('_');

  return {
    props: {
      title: `${niche?.replace('-', ' ')} in ${country?.toUpperCase()}`,
      description: `Latest ${niche} news and tools for ${country}`,
      slug,
    },
    revalidate: 60, // Rebuild every 60 seconds
  };
}

export default function DynamicPage({ title, description, slug }) {
  return (
    <>
      <Head>
        <title>{title} - RespireWork</title>
        <meta name="description" content={description} />
      </Head>
      <main style={{ padding: '2rem' }}>
        <h1>{title}</h1>
        <p>{description}</p>
        <p>This is a dynamic SEO page for <strong>{slug}</strong>.</p>
      </main>
    </>
  );
}
