import * as React from "react";

/** Tidal's monochrome diamond mark follows the surrounding text colour. */
export default function TidalLogo(props: React.SVGProps<SVGSVGElement>) {
  const { style, ...svgProps } = props;

  return (
    <svg
      viewBox="0 0 28 20"
      role="img"
      aria-label="Tidal"
      style={{
        display: "inline-block",
        height: "1em",
        verticalAlign: "-0.125em",
        width: "1.4em",
        ...style,
      }}
      {...svgProps}
    >
      <path
        fill="currentColor"
        d="m6 0 6 6-6 6-6-6L6 0Zm14 0 6 6-6 6-6-6 6-6ZM6 8l6 6-6 6-6-6 6-6Zm14 0 6 6-6 6-6-6 6-6Z"
      />
    </svg>
  );
}
