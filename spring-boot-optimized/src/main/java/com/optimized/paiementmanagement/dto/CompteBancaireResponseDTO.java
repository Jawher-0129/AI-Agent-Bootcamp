package com.optimized.paiementmanagement.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Bank Account Response DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompteBancaireResponseDTO {
    
    private Long id;
    private String numeroCompte;
    private BigDecimal solde;
    private String titulaire;
    private String typeCompte;
    private String status;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdDate;
}
