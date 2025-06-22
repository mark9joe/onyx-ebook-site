import Head from 'next/head';

export async function getStaticPaths() {
  return {
    paths: [],
    fallback: 'blocking',
  };
}

export async function getStaticProps({ params }) {
  const slug = params.slug || '';
  const [niche, country] = slug.split('_');

  return {
    props: {
      title: `${niche?.replace('-', ' ')} in ${country?.toUpperCase()}`,
      description: `Explore latest updates and resources on ${niche} in ${country}`,
      slug,
    },
    revalidate: 60,
  };
}

export default function DynamicPage({ title, description, slug }) {
  return (
    <>
      <Head>
        <title>{title} | RespireWork</title>
        <meta name="description" content={description} />
      </Head>
      <main style={{ padding: '2rem' }}>
        <h1>{title}</h1>
        <p>{description}</p>
        <p>This dynamic page was generated for: <strong>{slug}</strong></p>
      </main>
    </>
  );
}
